//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>

int s = 30;
int engine1 = 512;
int engine2 = 512;

void setup()
{
    Serial.begin(9600);
    SetPosition(1, engine1);
    SetPosition(2, engine2);
}

void loop()
{
   if (Serial.available() == 0){
      SetPosition(1, engine1);
      SetPosition(2, engine2);
      delay(10);
      return;
   }
   char c = Serial.read();
   if (c == '\0'){
      return;
   }
   Serial.println(c);
   if(c == 'n' || c == 'N'){
       nod(3, (c == 'N' ? 26 : 13), (c == 'N' ? 26 : 13));
    } else if(c == 's' || c == 'S'){
       shake(3, (c == 'S' ? 26 : 13), (c == 'S' ? 26 : 13));
     } else if (c == 'c'){
       center();
     } else if (c == 'r' || c == 'R'){
       engine1 = down_right(1, c == 'R' ? 26 : 13);
     } else if (c == 'l' || c == 'L'){
       engine1 = up_left(1, c == 'L' ? 26 : 13);
     } else if ( c == 'h') {
       char code[] = {'c', 'r', 'l', 'u', 'd', 'R', 'L', 'U', 'D', 'n', 'N', 's', 'S', 'e', 'E', 'q', 'Q', 'x', 'X', 'z', 'Z'};
       char *symbol[] = {"olarr", "rarr", "larr", "uarr", "darr", "rrarr", "llarr", "uuarr", "ddarr", "varr", "udarr", "harr", "lrarr", "nearr", "neArr", "nwarr", "nwArr", "searr", "seArr", "swarr", "swArr"};
       String codes = "[";
       for (int i = 0; i < sizeof(code) - 1; i++){
         codes = codes + "{\"code\":\"" + code[i] + "\",\"symbol\":\"&" + symbol[i] + ";\"},";
       }
       int j = sizeof(code) - 1;
       codes = codes + "{\"code\":\"" + code[j] + "\",\"symbol\":\"&" + symbol[j] + ";\"}]";       
       Serial.println(codes);
    }
}
 
// 1 step = 0.29
int up_left(int engine, int top){
  int j = (engine == 1 ? engine1 : engine2);
  top = top + j;
  while(j != top){
    j++;
    SetPosition(engine, j);
    delay(s);
  }
  return j;
}

int down_right(int engine, int top){
  int j = (engine == 1 ? engine1 : engine2);
  top = j - top;
  while(j != top){
    j--;
    SetPosition(engine, j);
    delay(s);
  }
  return j;
}

void center(){
  while(engine1 != 512 || engine2 != 512){
    if(engine1 != 512){
      if(engine1 > 512){ engine1--; } else { engine1++; }
      SetPosition(1, engine1);
    }
    if(engine2 != 512){
      if(engine2 > 512){ engine2--; } else { engine2++; }
      SetPosition(2, engine2);
    }
    delay(s);
  }
}

void nod(int t, int top, int down){
  int temp = engine2;
  engine2 = up_left(2, top);
  for(int i = 0; i < t; i++){
    engine2 = down_right(2, down * 2);
    engine2 = up_left(2, top * 2);
  }
  engine2 = down_right(2, down);
}

void shake(int t, int top, int down){
  int temp = engine1;
  engine1 = down_right(1, down);
  for(int i = 0; i < t; i++){
    engine1 = up_left(1, top * 2);  
    engine1 = down_right(1, down * 2);
  }
  engine1 = up_left(1, top);
}

