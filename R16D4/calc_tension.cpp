/*
 * Compiler : g++ main.cpp -o main
*/

#include <iostream>
#include <cstdlib>
#include <iterator>

constexpr int numberOfAOP {16};
constexpr int R {10'000};
constexpr float VCC {5.0f};
constexpr float threeshold {2.6f};
bool ledState[4];
int value {-1};

float measure_tension_aop(float vin, int n){
  float tension = vin * ((numberOfAOP - n) * R);
  tension /= (numberOfAOP * R);
  return tension;
}

int main(int argc, char* argv[]){
  float outputTension {0};

  if(argc < 2){
    std::cout << "Missing args (<vin>)\n";
    return -1;
  }

  float vin = std::atof(argv[1]);
  value = -1;

  // Affichage des tensions
  for(int i{1}; i <= numberOfAOP; ++i){
    outputTension = measure_tension_aop(VCC, i);
    std::cout << i << ": Tension = " << outputTension << "v\n";
    if(vin >= outputTension){
      value++;
    }
  }

  std::cout << "Value = " << value << '\n';

  /* ========= LED ======== */

  // Logique de D1
  if(value & 1){
    ledState[0] = true;
  }else{
    ledState[0] = false;
  }

  // Logique de D2
  value = value >> 1;
  if(value & 1){
    ledState[1] = true;
  }else{
    ledState[1] = false;
  }

  // Logique de D3
  value = value >> 1;
  if(value & 1){
    ledState[2] = true;
  }else{
    ledState[2] = false;
  }

  // Logique de D4
  value = value >> 1;
  if(value & 1){
    ledState[3] = true;
  } else{
    ledState[3] = false;
  }

	// Qu'une partie du flag
  std::cout << "404CTF{";
  for(int i{0}; i < std::size(ledState); ++i){
    if(ledState[i]){
      std::cout << "1";
    }else{
      std::cout << "0";
    }
  }

  std::cout << '\n';

  return 0;
}

