import math
import numpy as np
import multimedia_generator.utils as utils
from io import BytesIO
from pathlib import Path
from PIL import Image
from multimedia_generator.sld.sld_model import SLDFrameData, SLDFrame, SLDHeader, SLDSprite, SLDLayerData

NORMAL_COLOR_ALPHA = 224


def read_layer_header(layer_stream: BytesIO, has_size: bool) -> tuple[list, int, list]:
    coordinates = [utils.read_bytes(layer_stream, 2, signed=False) for _ in range(4) if has_size]
    flags = utils.read_bytes(layer_stream, 1, signed=False)
    layer_stream.seek(1, 1)
    draw_count = utils.read_bytes(layer_stream, 2, signed=False)
    draws = [utils.read_bytes(layer_stream, 1, signed=False) for _ in range(draw_count * 2)]
    return coordinates, flags, draws


def create_normal_layer(layer_stream: BytesIO, frame: SLDFrame, previous_frame: SLDFrame | None) -> SLDLayerData:
    coordinates, flags, draws = read_layer_header(layer_stream, True)
    data = np.zeros((frame.width * frame.height * 4,), dtype=np.uint8)
    if previous_frame is not None and flags & 0x80:
        previous_data = previous_frame.data.normal.image_data
        inherited = True
    else:
        previous_data = None
        inherited = False
    x0, y0, x1, y1 = coordinates
    draw_index = 0
    draw_number = draws[0]
    draw = False
    for y in range(y0, y1, 4):
        for x in range(x0, x1, 4):
            draw_number -= 1
            while draw_number < 0:
                draw_index += 1
                draw_number = draws[draw_index]
                draw = draw_index % 2
                draw_number -= 1
            if draw:
                raw_color0 = utils.read_bytes(layer_stream, 2, signed=False)
                raw_color1 = utils.read_bytes(layer_stream, 2, signed=False)
                color0 = utils.from_color_16(raw_color0)
                color1 = utils.from_color_16(raw_color1)
                indices = utils.read_bytes(layer_stream, 4, False)
                if raw_color0 > raw_color1:
                    colors = [
                        color0,
                        color1,
                        utils.mix_colors(color0, color1, 1.0 / 3.0),
                        utils.mix_colors(color0, color1, 2.0 / 3.0),
                    ]
                else:
                    colors = [
                        color0,
                        color1,
                        utils.mix_colors(color0, color1, 0.5),
                        None
                    ]
                for m in range(0, 4):
                    for n in range(0, 4):
                        i = m * 4 + n
                        current_color = colors[indices >> (i * 2) & 0x3]
                        utils.set_image_pixel(data, x + n + (y + m) * frame.width, current_color, NORMAL_COLOR_ALPHA)
            elif previous_data is not None:
                for m in range(0, 4):
                    offset = (x + (y + m) * frame.width) << 2
                    for n in range(0, 16):
                        data[offset] = previous_data[offset]
                        offset += 1
    return SLDLayerData(coordinates, inherited, data)


def create_shadow_layer(layer_stream: BytesIO, frame: SLDFrame, previous_frame: SLDFrame | None) -> SLDLayerData:
    coordinates, flags, draws = read_layer_header(layer_stream, True)
    data = np.zeros((frame.width * frame.height), dtype=np.uint8)
    previous_data = previous_frame.data.shadow.image_data if previous_frame is not None and flags & 0x80 else None
    x0, y0, x1, y1 = coordinates
    draw_index = 0
    draw_number = draws[0]
    draw = False
    for y in range(y0, y1, 4):
        for x in range(x0, x1, 4):
            draw_number -= 1
            while draw_number < 0:
                draw_index += 1
                draw_number = draws[draw_index]
                draw = draw_index % 2
                draw_number -= 1
            if draw:
                color0 = utils.read_bytes(layer_stream, 1, signed=False)
                color1 = utils.read_bytes(layer_stream, 1, signed=False)
                indices = [utils.read_bytes(layer_stream, 1, signed=False) for _ in range(6)]
                if color0 > color1:
                    colors = [
                        color0,
                        color1,
                        utils.mix_value(color0, color1, 1 / 7),
                        utils.mix_value(color0, color1, 2 / 7),
                        utils.mix_value(color0, color1, 3 / 7),
                        utils.mix_value(color0, color1, 4 / 7),
                        utils.mix_value(color0, color1, 5 / 7),
                        utils.mix_value(color0, color1, 6 / 7)
                    ]
                else:
                    colors = [
                        color0,
                        color1,
                        utils.mix_value(color0, color1, 1 / 5),
                        utils.mix_value(color0, color1, 2 / 5),
                        utils.mix_value(color0, color1, 3 / 5),
                        utils.mix_value(color0, color1, 4 / 5),
                        0,
                        255
                    ]
                for m in range(0, 4):
                    for n in range(0, 4):
                        i = m * 4 + n
                        vi = int(math.floor(i * 3 // 8))
                        ri = i * 3 % 8
                        current_color = colors[(indices[vi] | (indices[vi + 1] if vi < 5 else 0) << 8) >> ri & 0x7]
                        data[x + n + (y + m) * frame.width] = current_color
            elif previous_data is not None:
                for m in range(0, 4):
                    offset = x + (y + m) * frame.width
                    for n in range(0, 4):
                        data[offset] = previous_data[offset]
                        offset += 1
    return SLDLayerData(coordinates, False, data)


def adjust_frame_by_unknown_layer(frame: SLDFrame, layer_stream: BytesIO) -> None:
    image_data = frame.data.normal.image_data
    if not frame.data.normal.inherited:
        return
    coord = frame.data.normal.coordinates
    width = coord[2] - coord[0]
    height = coord[3] - coord[1]
    stride = frame.width
    right_limit = coord[2]

    rows = height // 4
    start_offset = 2 + rows * 2

    offsets = []
    for i in range(0, rows):
        ptr = i * 2 + 2
        offsets.append((layer_stream.getbuffer()[ptr] | layer_stream.getbuffer()[ptr + 1] << 8) + start_offset)
    offsets.append(len(layer_stream.getbuffer()))
    tile = 0
    for i in range(0, rows):
        off0 = offsets[i]
        off1 = offsets[i + 1]

        x_off = coord[0]
        y_off = i * 4 + coord[1]

        c = layer_stream.getbuffer()[off0] if off0 < len(layer_stream.getbuffer()) else 128
        if c < 128:
            x_off += c * 4
            off0 += 1
            c = layer_stream.getbuffer()[off0] if off0 < len(layer_stream.getbuffer()) else 128
        while c < 128:
            if c > 1:
                x_off += c * 4
            off0 += 1
            c = layer_stream.getbuffer()[off0] if off0 < len(layer_stream.getbuffer()) else 128
        slen = c - 128
        off0 += 1

        while off0 < off1:
            if slen <= 0:
                rep = layer_stream.getbuffer()[off0]
                off0 += 1
                c1 = layer_stream.getbuffer()[off0] if off0 < len(layer_stream.getbuffer()) else 128
                while c1 < 128:
                    if c1 > 1:
                        rep += c1
                    off0 += 1
                    c1 = layer_stream.getbuffer()[off0] if off0 < len(layer_stream.getbuffer()) else 128
                slen = c1 - 128
                if tile:
                    for k in range(0, rep):
                        for j in range(0, 16):
                            x = x_off + (j % 4)
                            if x < stride:
                                y = y_off + (j // 4)
                                o = 4 * (x + y * stride)
                                if tile & (1 << j) == 0:
                                    image_data[o + 3] = 0
                        x_off += 4
                        if x_off >= right_limit:
                            x_off = coord[0]
                            y_off += 4
                else:
                    for k in range(0, rep):
                        for j in range(0, 16):
                            x = x_off + (j % 4)
                            y = y_off + (j // 4)
                            o = 4 * (x + y * stride)
                            image_data[o + 3] = 0
                        x_off += 4
                        if x_off >= right_limit:
                            x_off = coord[0]
                            y_off += 4
                off0 += 1
                if off0 >= off1:
                    break

            x0 = x_off
            y0 = y_off
            tile = layer_stream.getbuffer()[off0] | layer_stream.getbuffer()[off0 + 1] << 8
            if tile:
                for j in range(0, 16):
                    x = x0 + (j % 4)
                    if x < stride:
                        y = y0 + (j // 4)
                        o = 4 * (x + y * stride)
                        if tile & (1 << j) == 0:
                            image_data[o + 3] = 0
            else:
                for j in range(0, 16):
                    x = x0 + (j % 4)
                    y = y0 + (j // 4)
                    o = 4 * (x + y * stride)
                    image_data[o + 3] = 0
            x_off += 4
            if x_off >= right_limit:
                x_off = coord[0]
                y_off += 4
            off0 += 2
            slen -= 1


def create_player_layer(layer_stream: BytesIO, frame: SLDFrame, previous_frame: SLDFrame | None) -> SLDLayerData:
    _, flags, draws = read_layer_header(layer_stream, False)
    coordinates = frame.data.normal.coordinates
    data = np.zeros((frame.width * frame.height), dtype=np.uint8)
    previous_data = previous_frame.data.player.image_data if previous_frame is not None and flags & 0x80 else None
    x0, y0, x1, y1 = coordinates
    draw_index = 0
    draw_number = draws[0]
    draw = False
    for y in range(y0, y1, 4):
        for x in range(x0, x1, 4):
            draw_number -= 1
            while draw_number < 0:
                draw_index += 1
                draw_number = draws[draw_index]
                draw = draw_index % 2
                draw_number -= 1
            if draw:
                color0 = utils.read_bytes(layer_stream, 1, signed=False)
                color1 = utils.read_bytes(layer_stream, 1, signed=False)
                indices = [utils.read_bytes(layer_stream, 1, signed=False) for _ in range(6)]
                if color0 > color1:
                    colors = [
                        color0,
                        color1,
                        utils.mix_value(color0, color1, 1 / 7),
                        utils.mix_value(color0, color1, 2 / 7),
                        utils.mix_value(color0, color1, 3 / 7),
                        utils.mix_value(color0, color1, 4 / 7),
                        utils.mix_value(color0, color1, 5 / 7),
                        utils.mix_value(color0, color1, 6 / 7)
                    ]
                else:
                    colors = [
                        color0,
                        color1,
                        utils.mix_value(color0, color1, 1 / 5),
                        utils.mix_value(color0, color1, 2 / 5),
                        utils.mix_value(color0, color1, 3 / 5),
                        utils.mix_value(color0, color1, 4 / 5),
                        0,
                        255
                    ]
                for m in range(0, 4):
                    for n in range(0, 4):
                        i = m * 4 + n
                        vi = int(math.floor(i * 3 // 8))
                        ri = i * 3 % 8
                        current_color = colors[(indices[vi] | (indices[vi + 1] if vi < 5 else 0) << 8) >> ri & 0x7]
                        data[x + n + (y + m) * frame.width] = current_color
            elif previous_data is not None:
                for m in range(0, 4):
                    offset = x + (y + m) * frame.width
                    for n in range(0, 4):
                        data[offset] = previous_data[offset]
                        offset += 1
    return SLDLayerData(coordinates, False, data)


def read_sprite_file(file_path: Path) -> SLDSprite | None:
    file_stream = BytesIO(file_path.read_bytes())
    file_stream.seek(0)
    file_format = utils.read_string_from_bytes(file_stream, 4)
    if file_format != 'SLDX':
        raise Exception("SLD Format is not valid")
    version = utils.read_bytes(file_stream, 2, signed=False)
    frame_count = utils.read_bytes(file_stream, 2, signed=False)
    unknown_1 = utils.read_bytes(file_stream, 4, signed=False)
    opacity = utils.read_bytes(file_stream, 4, signed=False)
    sld_header = SLDHeader(file_format, version, frame_count, unknown_1, opacity)
    if frame_count >= 4096:
        raise Exception(f"SLD file has too many frames: {frame_count} frames")
    frames = []
    previous_frame = None
    for i in range(frame_count):
        width = utils.read_bytes(file_stream, 2, signed=True)
        height = utils.read_bytes(file_stream, 2, signed=True)
        anchor_x = utils.read_bytes(file_stream, 2, signed=True)
        anchor_y = utils.read_bytes(file_stream, 2, signed=True)
        frame_type = utils.read_bytes(file_stream, 1, signed=False)
        unknown = utils.read_bytes(file_stream, 1, signed=False)
        index = utils.read_bytes(file_stream, 2, signed=True)
        sld_frame_data = SLDFrameData()
        frame = SLDFrame(width, height, anchor_x, anchor_y, frame_type, unknown, index, sld_frame_data)
        if frame_type & 0x01:
            frame.data.normal = create_normal_layer(utils.read_chunk(file_stream), frame, previous_frame)
        if frame_type & 0x02:
            frame.data.shadow = create_shadow_layer(utils.read_chunk(file_stream), frame, previous_frame)
        if frame_type & 0x04:
            unknown_layer = utils.read_chunk(file_stream)
            adjust_frame_by_unknown_layer(frame, unknown_layer)
        if frame_type & 0x08:
            frame.data.smudge = utils.read_chunk(file_stream)
        if frame_type & 0x10:
            frame.data.player = create_player_layer(utils.read_chunk(file_stream), frame, previous_frame)
        frames.append(frame)
        previous_frame = frame
    sprite = SLDSprite(sld_header, frames)
    return sprite


def frame_to_image(frame: SLDFrame, player_color: str) -> Image:
    player_color_list = utils.PLAYER_COLOR_MAP[player_color]
    image_data = frame.data.normal.image_data if frame.data.normal is not None else np.zeros((frame.width * frame.height * 4), dtype=np.uint8)
    limits = utils.update_image_limits([None, None, None, None], frame.data.normal.coordinates if frame.data.normal is not None else None)
    if frame.data.shadow is not None:
        shadow_data = frame.data.shadow.image_data
        limits = utils.update_image_limits(limits, frame.data.shadow.coordinates)
        for j in range(0, frame.height):
            for i in range(0, frame.width):
                alpha = shadow_data[i + j * frame.width]
                if alpha > 0:
                    offset = (i + j * frame.width) << 2
                    if image_data[offset + 3] < 128:
                        image_data[offset] = 0
                        image_data[offset + 1] = 0
                        image_data[offset + 2] = 0
                        image_data[offset + 3] = alpha
    if frame.data.player is not None:
        player_data = frame.data.player.image_data
        limits = utils.update_image_limits(limits, frame.data.player.coordinates)
        for j in range(0, frame.height):
            for i in range(0, frame.width):
                offset = (i + j * frame.width) << 2
                alpha0 = image_data[offset + 3]
                if alpha0 == NORMAL_COLOR_ALPHA:
                    alpha = player_data[i + j * frame.width]
                    if alpha > 0:
                        k = alpha / 255
                        r = image_data[offset]
                        g = image_data[offset + 1]
                        b = image_data[offset + 2]
                        brightness = 0.299 * r + 0.587 * g + 0.114 * b
                        p = player_color_list(brightness)
                        image_data[offset] = utils.mix_value(r, utils.clamp(p[0], 0, 255), k)
                        image_data[offset + 1] = utils.mix_value(g, utils.clamp(p[1], 0, 255), k)
                        image_data[offset + 2] = utils.mix_value(b, utils.clamp(p[2], 0, 255), k)
                        image_data[offset + 3] = 255
    converted_data = np.reshape(image_data, (frame.height, frame.width, 4))
    return Image.fromarray(converted_data), limits
