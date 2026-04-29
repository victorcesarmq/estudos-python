 /******************************************************************************

Welcome to GDB Online.
  GDB online is an online compiler and debugger tool for C, C++, Python, PHP, Ruby, 
  C#, OCaml, VB, Perl, Swift, Prolog, Javascript, Pascal, COBOL, HTML, CSS, JS
  Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <stdio.h>
#include <math.h>



int main(void)
{
    //Declaração de variaveis
    float nota1,nota2,AA,media;
    const float AM = 100;
 
    
    printf("----Calculando se 10 alunos diferentes foram aprovados ou não----\n\n");
    
    //Entrada de dados

    printf("\nDigite as nota do aluno \n");
    scanf("%f %f", &nota1, &nota2);
    printf("\nQuantas aulas o aluno  assistiu\n");
    scanf("%f", &AA);

    //Processamento 
    media = (nota1 + nota2) /2;
    
    //Condição para aprovação (Saída)
    if (media >= 6 && AA >= 75){
    printf("O aluno foi aprovado com uma media de %.1f, e assistiu %.f aulas\n", media,AA);
    printf("------------------------------------\n\n");    
    }
    //Condição para reprovação (Saída)
    else {
    printf("O aluno foi reprovado com uma media de %.1f, e assistiu a %.f aulas \n", media,AA);
    printf("------------------------------------\n\n");
    }
    


    return (0);
    }
