#include <stdio.h>
#include <math.h>

int main()
{
/* faça um programa em C, para ler dois numeros e simular uma calculadora, onde o usuario devera escolher uma resposta para a soma (subtração, divisão, raiz quadrada, adição, o dobro de um numero)*/
void soma(){
float valor1,valor2,result;
printf("Digite o valor 1 ");
scanf("%f", &valor1);
printf("Digite o valor 2");
scanf("%f", &valor2);
result = valor1 + valor2;
printf("\nO valor da soma é: %.2f", result);
}
void subtração(){
float valor1,valor2,result;
printf("Digite o valor 1 ");
scanf("%f", &valor1);
printf("Digite o valor 2");
scanf("%f", &valor2);
result = valor1 - valor2;
printf("\nO valor da soma é: %.2f", result);
}
void divisão(){
float valor1,valor2,result;
printf("Digite o valor 1 ");
scanf("%f", &valor1);
printf("Digite o valor 2");
scanf("%f", &valor2);
result = 0;
printf("\nO valor da soma é: %.2f", result);
}
void multiplicação(){
float valor1,valor2,result;
printf("Digite o valor 1 ");
scanf("%f", &valor1);
printf("Digite o valor 2");
scanf("%f", &valor2);
result = valor1 * valor2;
printf("\nO valor da soma é: %.2f", result);
}

void calculadora();
int escolha; 
printf("\n\nBem vindo a calculadora da IF\n\n");


printf("\n\n1.Soma\n");
printf("\n\n2.Divisão\n");
printf("\n\n3.multiplicação\n");
printf("\n\n4.subtração\n");
printf("\n\nOperação: ");
scanf("%d", &escolha); // armazena o numero 

switch (escolha){
    case 1 :
       soma ();
      break;
    case 2 :
       divisão ();
      break;
    case 3 :
       multiplicação();
      break;
    case 4 :
       subtração();
      break;
  }    
}
