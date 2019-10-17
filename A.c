#include<stdio.h>
#include<stdlib.h>

int main(void){
    char *all=NULL;
    int numberofcards=7,numberofsites=12;
    all=calloc((numberofcards+1),sizeof(char));


    while(1){
        for(int i=(numberofcards-1);i>=0;i--) printf("%d ",(int)all[i]);
        printf("\n");

        for(int i=0;i<=(numberofcards);i++){
            if(all[i]!=(numberofsites-1)){
                all[i]+=1;
                break;
            }
            else all[i]=0;
        }
        if((int)all[(numberofcards)]) break;
    }

    return 0;
}