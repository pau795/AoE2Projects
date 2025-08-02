string get_color(int player = 0){
	switch(player) {
        case 1 : {
            return ("<BLUE>");
        }
        case 2 : {
            return ("<RED>");
        }
        case 3 : {
            return ("<GREEN>");
        }
		case 4 : {
            return ("<YELLOW>");
        }
        case 5 : {
            return ("<AQUA>");
        }
        case 6 : {
            return ("<PURPLE>");
        }
		case 7 : {
            return ("<GREY>");
        }
        case 8 : {
            return ("<ORANGE>");
        }        
        default : {
            return ("");
        }
    }
	return ("");
}

void get_time(int player = 0){
	int total_secs = xsGetTime();
	int total_minutes = total_secs / 60;
	int hours = total_minutes / 60;
	int minutes = total_minutes % 60;
	int secs = total_secs % 60;
	
	string str_secs = "";
	if (secs > 9) str_secs = "" + secs;
	else str_secs = "0" + secs;
	
	string str_mins = ""; 
	if (minutes > 9) str_mins = "" + minutes;
	else str_mins = "0" + minutes;
	
	string str_hour = "";
	if (hours > 9) str_hour = "" + hours;
	else str_hour = "0" + hours;

    xsChatData(get_color(player) + "Tiempo final jugador " + player + ": " + str_hour + ":" + str_mins + ":" + str_secs);	
}


void get_time_1(){
	get_time(1);
}

void get_time_2(){
	get_time(2);
}

void get_time_3(){
	get_time(3);
}

void get_time_4(){
	get_time(4);
}

void get_time_5(){
	get_time(5);
}

void get_time_6(){
	get_time(6);
}

void get_time_7(){
	get_time(7);
}

void get_time_8(){
	get_time(8);
}
