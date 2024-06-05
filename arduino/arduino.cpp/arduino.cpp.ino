#include <Arduino.h>
#include <math.h>
#define LEVEL 676
#define END_BYTES 8
#define BEGIN_BYTES 0


const int selectionLine[] = {2, 3, 4, 5, 6, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40};
const int dataLine[] = {A0, A1, A2, A3, A4, A5, A6, A7};
const bool CE_control = 0; // When LOW, selects the chip. When HIGH, deselects the chip
const bool OE_control = 0; // Output Enable. Controls the direction of the I/O pins. When LOW, the I/O pins behave as outputs. When deasserted HIGH, I/O pins are tristated, and act as input data pins
const bool WE_control = 1; // When selected LOW, a WRITE is conducted. When selected HIGH, a READ is conducted
const int CE = 48;
const int OE = 50;
const int WE = 52;
char resultASCII[100] ={-1};
int resultPtr = 0;

int seccess = 0; // secceful number
int times = 0;   // total number

bool first_data[END_BYTES - BEGIN_BYTES][8];
bool second_data[END_BYTES - BEGIN_BYTES][8];

void setup()
{
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(WE, OUTPUT);
  digitalWrite(WE, WE_control);
  pinMode(CE, OUTPUT);
  digitalWrite(CE, CE_control);
  pinMode(OE, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(OE, OE_control);

  // selection line pin mode
  for (int i = 0; i < 8; i++)
  {
    pinMode(selectionLine[i], OUTPUT);
    digitalWrite(selectionLine[i], 0);
  }

  // dataline pin mode
  for (int i = 0; i < 8; i++)
  {
    pinMode(dataLine[i], INPUT);
  }
  for (int i = 0; i < 15; i++)
  {
    digitalWrite(selectionLine[i], 0);
  }
  for (int i = 0; i < 10; i++)
  {
    digitalWrite(13, 1);
    delay(100);
    digitalWrite(13, 0);
    delay(100);
  }
}

void readAnalogData()
{
  for (int i = 0; i < 8; i++)
  {
    double temp = analogRead(dataLine[i]);
    Serial.print(temp * 5 / 1023);
    Serial.print("\t");
  }
  int sum =0;
  
  Serial.println();
}
int readDigitalData()
{
  int sum = 0;
  for (int i = 0; i < 8; i++)
  {
    int temp = analogRead(dataLine[i]);
    if (temp >= LEVEL * 0.5){
      Serial.print("1");
      sum += pow(2,i);
    }
      
    else
    {
        Serial.print("0");
    }
    //Serial.print(" ");
  }
  //Serial.print(sum);
  //Serial.println();
  return sum;
}

void pushData(int line)
{
  for (int i = 0; i < 8; i++)
  {
    
    int temp = analogRead(dataLine[i]);
    if (temp >= LEVEL * 0.5)
      first_data[line][i] = 1;
    else
      first_data[line][i] = 0;
  }
}

// bool compare()
// {
//   for (int i = 0; i < END_BYTES - BEGIN_BYTES; i++)
//   {
//     for (int j = 0; j < 8; j++)
//     {
//       if (first_data[i][j] != second_data[i][j])
//       {
//         return 0;
//       }
//     }
//   }
//   return 1;
// }

// void copy()
// {
//   for (int i = 0; i < END_BYTES - BEGIN_BYTES; i++)
//   {
//     for (int j = 0; j < 8; j++)
//     {
//       second_data[i][j] = first_data[i][j];
//     }
//   }
// }
void pufTest()
{
  // change selection line signal
//  for (int i = BEGIN_BYTES; i < END_BYTES/2; i++)
//  {
//      for(int j = END_BYTES/2; j<END_BYTES; j++){
//      // read digital data
//      
//      digitalWrite(selectionLine[i], 1);
//      digitalWrite(selectionLine[j], 1);
//    
//      // read every 8 bit
//      readDigitalData();
//      pushData(i);
//      digitalWrite(selectionLine[i], 0);
//      digitalWrite(selectionLine[j], 0);
//    }
//
//  }

  // bool i=false, j=false, k=false,l=false,m=false,n=false,o=false,p=false;
  bool carry = false;
  boolean val[8] = {0};
  for(int count =0; count<256; count++){
    
    if(val[0] == false){
      val[0] = true;
      carry = false;
    }
    else{
      val[0] = false;
      carry = true;
    }

    if(carry = true){
      if(val[1] == false){
        val[1] = true;
        carry = false;
      }
      else{
        val[1] = false;
        carry = true;
      }
    }

     if(carry == true){
      if(val[2] == false){
        val[2] = true;
        carry = false;
      }
      else{
        val[2] = false;
        carry = true;
      }
    }

     if(carry == true){
      if(val[3] == false){
        val[3] = true;
        carry = false;
      }
      else{
        val[3] = false;
        carry = true;
      }
    }
    if(carry == true){
      if(val[4] == false){
        val[4] = true;
        carry = false;
      }
      else{
        val[4] = false;
        carry = true;
      }
    }

    if(carry == true){
      if(val[5] == false){
        val[5] = true;
        carry = false;
      }
      else{
        val[5] = false;
        carry = true;
      }
    }

    if(carry == true){
      if(val[6] == false){
        val[6] = true;
        carry = false;
      }
      else{
        val[6] = false;
        carry = true;
      }
    }
    if(carry == true){
      if(val[7] == false){
        val[7] = true;
        carry = false;
      }
      else{
        val[7] = false;
        carry = true;
      }
    }

    for(int i=0; i<8; i++){
      digitalWrite(selectionLine[i], val[i]);
      pushData(i);
    }
    readDigitalData();

//    ofstream myfile;
//    myfile.open("example.txt");
//    int sum = readDigitalData();
//    myfile<<"sum"<<" ";
//    myfile.close();

  }
  

  Serial.println("");
  // analog data
  // for (int i = BEGIN_BYTES; i < END_BYTES; i++)
  // {
  //   digitalWrite(selectionLine[i], 1);
  //   // read every 8 bit
  //   readAnalogData();
  //   digitalWrite(selectionLine[i], 0);
  // }
  // for (int i = BEGIN_BYTES; i < END_BYTES/2; i++)
  // {
  //   for(int j = END_BYTES/2; j<END_BYTES; j++){
  //     digitalWrite(selectionLine[i],1);
  //     digitalWrite(selectionLine[j],1);
  //     readAnalogData();
  //     digitalWrite(selectionLine[i],0);
  //     digitalWrite(selectionLine[j],0);
  //   }
  //   // digitalWrite(selectionLine[i], 1);
  //   // // read every 8 bit
  //   // readAnalogData();
  //   // digitalWrite(selectionLine[i], 0);
  // }
  // for(int i=0; i<100; i++){
  //   Serial.print(resultASCII[i]);
  // }

  // compare if two data same
  // if (compare() == 1)
  // {
  //   Serial.println("compare");
  //   seccess++;
  // }
  // else
  // {
  //   Serial.println("not compare");
  // }
  // copy();
  // Serial.println((double)seccess / times);
}

void loop()
{
  times++;
  //Serial.println(LEVEL / 2);
  digitalWrite(7, 1);
  delay(1000);
  pufTest();

  digitalWrite(7, 0);
  delay(1000);
  // Serial.print("123");
}
