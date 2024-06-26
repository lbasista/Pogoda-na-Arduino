#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Zmienne do przechowywania prognozy
String temp = "";
String opis = "";
String temp_jutro = "";
String opis_jutro = "";

unsigned long o_odswiezenie = 0;
const unsigned long interwal = 10000; //Interwał odświeżania ekranu

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2); //Wielkość wyświetlacza (16 wierszy x 2 kolumny)
  lcd.setCursor(0, 0);
  lcd.print("Uruchamianie");
  lcd.setCursor(0, 1);
  lcd.print("Prosze czekac");
}

void loop()
{
  if(Serial.available()>0)
  {
    //Podział danych na kategorie
    String prognoza = Serial.readStringUntil(';');

    int separatordzis = prognoza.indexOf(' ');
    int nlinia = prognoza.indexOf('\n');
    int separatorjutro = prognoza.indexOf(' ', nlinia + 1);

    temp = prognoza.substring(0, separatordzis);
    opis = prognoza.substring(separatordzis + 1, nlinia);
    temp_jutro = prognoza.substring(nlinia + 1, separatorjutro);
    opis_jutro = prognoza.substring(separatorjutro + 1);
  }
    //Wyświetlanie
  unsigned long uruchomiony = millis();
  if (uruchomiony - o_odswiezenie >= interwal)
  {
    o_odswiezenie = uruchomiony;
    //Dzisiaj
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Temp: " + temp + (char)223 + "C");
    lcd.setCursor(0,1);
    lcd.print(opis);
    delay(7500);
    //Jutro
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(">Temp: " + temp_jutro + (char)223 + "C");
    lcd.setCursor(0,1);
    lcd.print(opis_jutro);
    delay(7500);
  }
}