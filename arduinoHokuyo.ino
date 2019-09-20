#include <Adafruit_NeoPixel.h>
#include <Servo.h> 

#define SERBOPIN 3
#define SWITCH 5
#define LEDPIN 13
#define NUM_LIGHTS 200 //트램폴린 지름으로 따지면 대충 200개 조금 안된다.
//첫번째 인자값은 네오픽셀의 LED의 개수
//두번째 인자값은 네오픽셀이 연결된 아두이노의 핀번호
//세번째 인자값은 네오픽셀의 타입에 따라 바뀌는 flag
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LIGHTS, LEDPIN, NEO_GRB + NEO_KHZ800);
Servo servo; 


int a = 0;
char ch;
int angle = 0; // servo position in degrees 


//rgb변수 선언
uint8_t r = 0;
uint8_t g = 0;
uint8_t b = 0;
uint32_t color;
uint32_t colorTemp;


void setup() {
  Serial.begin(9600);
  strip.begin(); //네오픽셀을 초기화하기 위해 모든LED를 off시킨다
  strip.show();
  servo.attach(servoPin); 
  servo.write(0);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(SWITCH, INPUT);
  Serial.println("arduino - successful connection|");
}

//NeoPixel에 달린 LED를 각각 주어진 인자값 색으로 채워나가는 함수
void colorWipe(uint32_t c, int count) {
  for (uint16_t i = 0; i < count; i++) {
    strip.setPixelColor(i, c);
  }
  strip.show();
}


void loop() {
  a = digitalRead(SWITCH);
  if(a == 1){
    String trash = Serial.readStringUntil('|');
    String inString = "";
    Serial.println("a|");


    servo.write(80);
    delay(1000);
    servo.write(0);

    
    //delay(2000);
    while(1)
    {
      if(Serial.available()){
       inString = Serial.readStringUntil('|');
       break;
      };
    }
    Serial.println(inString + "|");
    delay(1000);
    int value = map(inString.toInt(), 0, 2000, 0, 50);
    colorWipe(strip.Color(255, 0, 0), value); //빨간색 출력
    delay(4000);
    colorWipe(strip.Color(0, 0, 0), value); //빨간색 출력

  };
}
