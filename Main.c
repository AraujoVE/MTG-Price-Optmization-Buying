#include<stdio.h>
#include<stdlib.h>
#include<time.h>

///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
float **AppendFromTxt(float ****BaseStructureAd,int **CardsStudiedAd,int *realcards,int *manycards,int *manysites){
    FILE *readf= fopen("summary.txt","r");
    fscanf(readf,"%d %d %d",&(*manysites),&(*realcards),&(*manycards));
    (*CardsStudiedAd)=calloc((*realcards),sizeof(int));
    (*BaseStructureAd)=malloc((*manysites)*sizeof(float**));
    for(int i=0;i<(*manysites);i++) (*BaseStructureAd)[i]=malloc(((*realcards)+1)*sizeof(float*));
    
    for(int i=0;i<(*realcards);i++){
        fscanf(readf,"%d ",&((*CardsStudiedAd)[i]));
        for(int j=0;j<(*manysites);j++) (*BaseStructureAd)[j][i]=calloc(((*CardsStudiedAd)[i]),sizeof(float));
    }
    for(int j=0;j<(*manysites);j++) (*BaseStructureAd)[j][(*realcards)]=calloc(2,sizeof(float));

    
    for(int i=0;i<(*manysites);i++){
        for(int j=0;j<(*realcards);j++){
            for(int k=0;k<((*CardsStudiedAd)[j]);k++) fscanf(readf,"%f ",&((*BaseStructureAd)[i][j][k]));
        }
        fscanf(readf,"%f ",&((*BaseStructureAd)[i][(*realcards)][0]));
        fscanf(readf,"%f ",&((*BaseStructureAd)[i][(*realcards)][1]));
    }
    fclose(readf);
    for(int k=0;k<(*manysites);k++){
        for(int i=0;i<(*realcards);i++){
            for(int j=0;j<(*CardsStudiedAd)[i];j++){
                if((*BaseStructureAd)[k][i][j]==0) (*BaseStructureAd)[k][i][j]=1000000; 
            }
        }
    }
}
///////////////////////////////////////////////////////////////////////////////////////////////////
void CreateAll(int *CardsStudied,float ****DecodedListAd,float **FitnessAd, float **FitnessAd2,int ***quantitylistAd,int ***quantitylistAd2,int ***siteslistAd,int ***siteslistAd2,int manyparentals,int manycards,int manysites,int realcards){

    *DecodedListAd=malloc(realcards*sizeof(float**));
    *FitnessAd=calloc(manyparentals,sizeof(float));
    *FitnessAd2=calloc(manyparentals,sizeof(float));
    *quantitylistAd=malloc((manyparentals)*sizeof(int*));
    *quantitylistAd2=malloc((manyparentals)*sizeof(int*));
    *siteslistAd=malloc((manyparentals)*sizeof(int*));
    *siteslistAd2=malloc((manyparentals)*sizeof(int*));

    for(int i=0;i<realcards;i++){
        (*DecodedListAd)[i]=malloc((CardsStudied[i])*sizeof(float*));
        for(int j=0;j<(CardsStudied[i]);j++) (*DecodedListAd)[i][j]=calloc(2,sizeof(float));
    }

    for(int i=0;i<manyparentals;i++){
        (*quantitylistAd)[i]=calloc((manycards+1),sizeof(int));
        (*quantitylistAd2)[i]=calloc((manycards+1),sizeof(int));
        (*siteslistAd)[i]=calloc(manysites,sizeof(float));
        (*siteslistAd2)[i]=calloc(manysites,sizeof(float));
    }
}
///////////////////////////////////////////////////////////////////////////////////////////////////
void ManyParentalsStart(int manysites,int m,int manycards,int ***quantitylistAd,int *allsites,int ***siteslistAd){
    int torand=manysites,randpart,numberofsites;
    numberofsites=(rand()%(manycards))+1;
    if(numberofsites>manysites) numberofsites=manysites;
    (*quantitylistAd)[m][0]=numberofsites;
    for(int i=1;i<=numberofsites;i++){
        randpart=rand()%(torand);
        (*quantitylistAd)[m][i]=allsites[randpart];
        (*siteslistAd)[m][(allsites[randpart])]=1;
        torand-=1;
        allsites[randpart]=allsites[torand];
        allsites[torand]=(*quantitylistAd)[m][i];
    }
}

void CrossoverStart(int m,int manysites,int ***siteslistAd2,int ***quantitylistAd,int ***quantitylistAd2){
    int torand,randpart,pos=1, theswap,numberofsites;    
    int members[2]={0};

    for(int i=0;i<manysites;i++) (*siteslistAd2)[m][i]=0;

    if(((*quantitylistAd)[0][0]%2)&&((*quantitylistAd)[m][0]%2)) members[(rand()%2)]=1;
    else if((*quantitylistAd)[0][0]%2) members[0]=(rand()%2);
    else if((*quantitylistAd)[m][0]%2) members[1]=(rand()%2);

    numberofsites=(((*quantitylistAd)[0][0])/2)+(((*quantitylistAd)[m][0])/2)+members[0]+members[1];

    torand=(*quantitylistAd)[0][0];
    for(int i=0;i<(((*quantitylistAd)[0][0]/2)+members[0]);i++){
        randpart=1+rand()%(torand);
        theswap=(*quantitylistAd)[0][randpart];
        if(!((*siteslistAd2)[m][theswap])){
            (*quantitylistAd2)[m][pos]=theswap;
            pos+=1;
            (*siteslistAd2)[m][theswap]=1;
        }

        (*quantitylistAd)[0][randpart]=(*quantitylistAd)[0][torand];
        (*quantitylistAd)[0][torand]=theswap;
        torand-=1;
    }

    torand=(*quantitylistAd)[m][0];
    for(int i=0;i<(((*quantitylistAd)[m][0]/2)+members[1]);i++){
        randpart=1+rand()%(torand);
        theswap=(*quantitylistAd)[m][randpart];
        if(!((*siteslistAd2)[m][theswap])){
            (*quantitylistAd2)[m][pos]=theswap;
            pos+=1;
            (*siteslistAd2)[m][theswap]=1;
        }

        (*quantitylistAd)[m][randpart]=(*quantitylistAd)[m][torand];
        (*quantitylistAd)[m][torand]=theswap;
        torand-=1;
    }

    (*quantitylistAd2)[m][0]=pos-1;

}

void MutationStart(int m,int ***quantitylistAd,int mutation,int ***siteslistAd,int manysites,int *allsites){
    int variable=0,torand,randpart,theswap,newrand;    

    torand=(*quantitylistAd)[m][0];
    while((mutation>variable) && (torand>variable)){
        randpart=1+rand()%(torand-variable);
        (*siteslistAd)[m][((*quantitylistAd)[m][randpart])]=0;
        newrand=rand()%(manysites-variable);
        if((*siteslistAd)[m][(allsites[newrand])]){
            (*quantitylistAd)[m][randpart]=(*quantitylistAd)[m][(torand-variable)];
            (*quantitylistAd)[m][(torand-variable)]=(*quantitylistAd)[m][((*quantitylistAd)[m][0])];
            (*quantitylistAd)[m][((*quantitylistAd)[m][0])]=0;
            (*quantitylistAd)[m][0]-=1;
            theswap=allsites[newrand];            
            allsites[newrand]=allsites[(manysites-variable-1)];
            allsites[(manysites-variable-1)]=theswap;
        }
        else{
            (*siteslistAd)[m][(allsites[newrand])]=1;
            (*quantitylistAd)[m][randpart]=(*quantitylistAd)[m][(torand-variable)];
            (*quantitylistAd)[m][(torand-variable)]=allsites[newrand];
            allsites[newrand]=allsites[(manysites-variable-1)];
            allsites[(manysites-variable-1)]=(*quantitylistAd)[m][(torand-variable)];
        }
        variable+=1;
    }

}
///////////////////////////////////////////////////////////////////////////////////////////////////
void ParentalGeneration(int initial,int manysites,int manyparentals,float **FitnessAd,int manycards, int ***quantitylistAd,int ***siteslistAd,float ***BaseStructure,int realcards,int *CardsStudied){
    int *provisoryArray;
    int therand,position,randpos,theswap,increases,numberofsites;
    int *allsites=calloc(manysites,sizeof(int));
    int *turninto;
    int *Shipps;
    for(int i=0;i<manysites;i++) allsites[i]=i;


    for(int m=initial;m<manyparentals;m++){
        turninto=calloc((manycards+1),sizeof(int));
        (*FitnessAd)[m]=0;
        position=-1;
        ManyParentalsStart(manysites,m,manycards,quantitylistAd,allsites,siteslistAd);
        Shipps=calloc(manysites,sizeof(int));
        for(int n=0;n<realcards;n++){
            provisoryArray=calloc(manysites,sizeof(int));
            for(int o=0;o<CardsStudied[n];o++){
                position+=1;
                therand=(*quantitylistAd)[m][1];
                for(int i=2;i<=((*quantitylistAd)[m][0]);i++){
                    if(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])>(BaseStructure[((*quantitylistAd)[m][i])][n][(provisoryArray[((*quantitylistAd)[m][i])])]*BaseStructure[((*quantitylistAd)[m][i])][realcards][1]))||(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])==(BaseStructure[((*quantitylistAd)[m][i])][n][(provisoryArray[((*quantitylistAd)[m][i])])]*BaseStructure[((*quantitylistAd)[m][i])][realcards][1]))&&(rand()%2))){
                        therand=(*quantitylistAd)[m][i];        
                    }
                }
                if(!(Shipps[therand])){
                    Shipps[therand]=1;
                    (*FitnessAd)[m]+=BaseStructure[therand][realcards][0];
                    turninto[(turninto[0]+1)]=therand;
                    turninto[0]+=1;        
                }
                (*FitnessAd)[m]+=BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1];

                provisoryArray[therand]+=1;
            }
            free(provisoryArray);
        }
        for(int i=0;i<=(turninto[0]);i++){
            (*quantitylistAd)[m][i]=turninto[i];        
        }
        free(Shipps);
        free(turninto);
    }
    free(allsites);
}
void MutationGeneration(int manysites,int manyparentals,float **FitnessAd,int mutation,int manycards, int ***quantitylistAd,int ***siteslistAd,float ***BaseStructure,int realcards,int *CardsStudied){
    int *provisoryArray;
    int therand,position,randpos,theswap,increases,numberofsites;
    int *Shipps;
    int *allsites=calloc(manysites,sizeof(int));
    int *turninto;

    for(int i=0;i<manysites;i++) allsites[i]=i;


    for(int m=1;m<manyparentals;m++){
        turninto=calloc((manycards+1),sizeof(int));
        (*FitnessAd)[m]=0;
        position=-1;
        MutationStart(m,quantitylistAd,mutation,siteslistAd,manysites,allsites);
        Shipps=calloc(manysites,sizeof(int));
        for(int n=0;n<realcards;n++){
            provisoryArray=calloc(manysites,sizeof(int));
            for(int o=0;o<CardsStudied[n];o++){
                position+=1;
                therand=(*quantitylistAd)[m][1];
                for(int i=2;i<=((*quantitylistAd)[m][0]);i++){
                    if(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])>(BaseStructure[((*quantitylistAd)[m][i])][n][(provisoryArray[((*quantitylistAd)[m][i])])]*BaseStructure[((*quantitylistAd)[m][i])][realcards][1]))||(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])==(BaseStructure[((*quantitylistAd)[m][i])][n][(provisoryArray[((*quantitylistAd)[m][i])])]*BaseStructure[((*quantitylistAd)[m][i])][realcards][1]))&&(rand()%2))){
                        therand=(*quantitylistAd)[m][i];        
                    }
                }
                if(!(Shipps[therand])){
                    Shipps[therand]=1;
                    (*FitnessAd)[m]+=BaseStructure[therand][realcards][0];        
                    turninto[(turninto[0]+1)]=therand;
                    turninto[0]+=1;        
                }
                (*FitnessAd)[m]+=BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1];

                provisoryArray[therand]+=1;
            }
            free(provisoryArray);
        }
        for(int i=0;i<=(turninto[0]);i++){
            (*quantitylistAd)[m][i]=turninto[i];        
        }
        free(Shipps);
        free(turninto);
    }
    free(allsites);
}
void CrossoverGeneration(int manysites,int manyparentals,float **FitnessAd, int ***siteslistAd2,int ***quantitylistAd2,int manycards, int ***quantitylistAd,int ***siteslistAd,float ***BaseStructure,int realcards,float **FitnessAd2,int *CardsStudied){
    int *provisoryArray;
    int therand,position,randpos,theswap,increases,numberofsites;
    int *Shipps;
    void *theswapAd=NULL;
    int *turninto;
    int *allsites=calloc(manysites,sizeof(int));
    for(int i=0;i<manysites;i++) allsites[i]=i;
    int realq=0;
    (*FitnessAd2)[0]=(*FitnessAd)[0];
    for(int i=0;i<=(*quantitylistAd)[0][0];i++) (*quantitylistAd2)[0][i]=(*quantitylistAd)[0][i]; 


    for(int m=1;m<manyparentals;m++){
        turninto=calloc((manycards+1),sizeof(int));
        (*FitnessAd2)[m]=0;
        position=-1;
        CrossoverStart(m,manysites,siteslistAd2,quantitylistAd,quantitylistAd2);
        Shipps=calloc(manysites,sizeof(int));
        for(int n=0;n<realcards;n++){
            provisoryArray=calloc(manysites,sizeof(int));
            for(int o=0;o<CardsStudied[n];o++){
                position+=1;
                therand=(*quantitylistAd2)[m][1];
                for(int i=2;i<=((*quantitylistAd2)[m][0]);i++){
                    if(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])>(BaseStructure[((*quantitylistAd2)[m][i])][n][(provisoryArray[((*quantitylistAd2)[m][i])])]*BaseStructure[((*quantitylistAd2)[m][i])][realcards][1]))||(((BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])==(BaseStructure[((*quantitylistAd2)[m][i])][n][(provisoryArray[((*quantitylistAd2)[m][i])])]*BaseStructure[((*quantitylistAd2)[m][i])][realcards][1]))&&(rand()%2))){
                        therand=(*quantitylistAd2)[m][i];        
                    }
                }
                if(!(Shipps[therand])){
                    Shipps[therand]=1;
                    (*FitnessAd2)[m]+=BaseStructure[therand][realcards][0];        
                    turninto[(turninto[0]+1)]=therand;
                    turninto[0]+=1;        
                }
                (*FitnessAd2)[m]+=BaseStructure[therand][n][(provisoryArray[therand])]*BaseStructure[therand][realcards][1];

                provisoryArray[therand]+=1;
            }
            free(provisoryArray);
        }
        for(int i=0;i<=(turninto[0]);i++){
            (*quantitylistAd2)[m][i]=turninto[i];        
        }
        free(Shipps);
        free(turninto);
    }
    free(allsites);


    theswapAd=(*quantitylistAd);
    (*quantitylistAd)=(*quantitylistAd2);
    (*quantitylistAd2)=theswapAd;

    theswapAd=(*siteslistAd);
    (*siteslistAd)=(*siteslistAd2);
    (*siteslistAd2)=theswapAd;

    theswapAd=(*FitnessAd);
    (*FitnessAd)=(*FitnessAd2);
    (*FitnessAd2)=theswapAd;

    theswapAd=NULL;
    free(theswapAd);
}
///////////////////////////////////////////////////////////////////////////////////////////////////
void FindBestWorst(float *Fitness,float *Fitness2,int **quantitylist,int **quantitylist2,int **siteslist,int **siteslist2,int manyparentals,int manycards,int manysites,int *last,int posi,int best){
    int minmax=0,change=0;
    float theswapf;
    void *theswapv=NULL;
    
    for(int i=1;i<manyparentals;i++){
        if((Fitness[minmax]>Fitness[i])&&(best)) minmax=i;
        if((Fitness[minmax]<Fitness[i])&&(!best)) minmax=i;
    }
    if(!best) change=manyparentals-1;
    if(((minmax)&&(best))||((minmax!=(manyparentals-1))&&(!best))){
        //printf("..\n");
        if(best) (*last)=posi;

        theswapf=Fitness[change];
        Fitness[change]=Fitness[minmax];
        Fitness[minmax]=theswapf;


        theswapv=quantitylist[change];
        quantitylist[change]=quantitylist[minmax];
        quantitylist[minmax]=theswapv;

        theswapv=siteslist[change];
        siteslist[change]=siteslist[minmax];
        siteslist[minmax]=theswapv;
    }
    theswapv=NULL;
    free(theswapv);
}
int Evaluation(int **quantitylist,float *PreviousBest, float *Fitness, int *mutation,int *occurences,int manyparentals,int xaxis,int mutationtax,int genocidetax,clock_t *end){
    float average=0;
    int wrongs=0;
    FILE *filem= fopen("coordinates.txt","a+");

    for(int i=0;i<manyparentals;i++){
        if(Fitness[i]<1000000) average+=Fitness[i];
        else wrongs+=1;
    }
    average/=(manyparentals-wrongs);



    if(((*PreviousBest)>Fitness[0])&&(Fitness[0])){//novo melhor de todos

        fprintf(filem,"%d/%0.2f/%0.2f/%d/A/\n",xaxis,Fitness[0],average,wrongs);
        fclose(filem);

        //printf(".\n");
        //printf("xx\n");

        (*PreviousBest)=Fitness[0];
        (*mutation)=0;
        (*occurences)=0;
        *end = clock();
        printf("//%f: ",(*PreviousBest));
        for(int i=1;i<=quantitylist[0][0];i++) printf("%d ",quantitylist[0][i]);
        printf("\n");

        return 0;
    }
    else{
        (*occurences)+=1;

        if((*occurences)%mutationtax){//nada aconteceu
            fprintf(filem,"%d/%0.2f/%0.2f/%d/B/\n",xaxis,Fitness[0],average,wrongs);
            fclose(filem);

            return 1;
        }
        else{
            (*mutation)+=1;
            if(!((*occurences)%(mutationtax*genocidetax))){//genocidio
                fprintf(filem,"%d/%0.2f/%0.2f/%d/C/\n",xaxis,Fitness[0],average,wrongs);
                fclose(filem);

                (*mutation)=1;
                return 2;        
            }
            else{//aumento da população
                fprintf(filem,"%d/%0.2f/%0.2f/%d/D/\n",xaxis,Fitness[0],average,wrongs);
                fclose(filem);

                return 3;
            }
        }
    }
}
void PredationGeneration(float ***BaseStructure,float **FitnessAd,float **Fitness2Ad,int ***quantitylistAd,int ***quantitylist2Ad,int ***siteslistAd,int ***siteslist2Ad,int manysites,int manyparentals,int manycards,int realcards,int *CardsStudied,int *lastAd){
    FindBestWorst(*FitnessAd,*Fitness2Ad,*quantitylistAd,*quantitylist2Ad,*siteslistAd,*siteslist2Ad,manyparentals,manycards,manysites,lastAd,0,0);
    ParentalGeneration((manyparentals-1),manysites,manyparentals,FitnessAd,manycards,quantitylistAd,siteslistAd,BaseStructure,realcards,CardsStudied);
}
void FreeForAll(float ****DecodedListAd,float ****BaseStructureAd,float **FitnessAd,float **Fitness2Ad,int ***quantitylistAd,int ***quantitylist2Ad,int ***siteslistAd,int ***siteslist2Ad,int **CardsStudiedAd,int manycards,int realcards,int manysites,int manyparentals){
    
    for(int i=0;i<realcards;i++){
        for(int j=0;j<(*CardsStudiedAd)[i];j++){
            free((*DecodedListAd)[i][j]);
        }
        free((*DecodedListAd)[i]);
    }
    free(*DecodedListAd);




    for(int i=0;i<manysites;i++){
        for(int j=0;j<=realcards;j++){
            free((*BaseStructureAd)[i][j]);
        }
        free((*BaseStructureAd)[i]);
    }    
    free(*BaseStructureAd);

    for(int i=0;i<manyparentals;i++){
        free((*quantitylistAd)[i]);
        free((*quantitylist2Ad)[i]);
        free((*siteslistAd)[i]);
        free((*siteslist2Ad)[i]);
    }
    free(*FitnessAd);
    free(*Fitness2Ad);
    free(*quantitylistAd);
    free(*quantitylist2Ad);
    free(*siteslistAd);
    free(*siteslist2Ad);
    free(*CardsStudiedAd);
}
/*
void PrintAll(int manyparentals,int **quantitylist,float *Fitness,int realcards,int *CardsStudied,float ***BaseStructure,int last){
    int position;
    for(int i=0;i<manyparentals;i++){
        printf("%d #%d#\n",i,quantitylist[i][0]);
        for(int j=1;j<=(quantitylist[i][0]);j++) printf("%d ",quantitylist[i][j]);
        printf("Fitness of (%d): %f\n",i,Fitness[i]);
    }
    position=-1;
    for(int i=0;i<realcards;i++){
        printf("Card %d:\t",i);
        for(int j=0;j<CardsStudied[i];j++){
            position+=1;
            printf(" %f(%f)",FullList[0][position],BaseStructure[(int)(FullList[0][position])][i][0]);
        }
        printf("\n");
    }

    for(int i=1;i<=(quantitylist[0][0]);i++){
        printf("%d: %f(%f)\n",quantitylist[0][i],BaseStructure[(quantitylist[0][i])][realcards][0],BaseStructure[(quantitylist[0][i])][realcards][1]);
    }
    printf("\nBest Fitness: %f\tlast:%d\n\n",Fitness[0],last);
    
}
*/
void DecodeBestOnes(int manysites,int realcards,int *CardsStudied,int **quantitylist,float ***BaseStructure,float ***DecodedList){
    int *provisoryArray=NULL;
    int therand;
    for(int i=0;i<realcards;i++){
        provisoryArray=calloc(manysites,sizeof(int));
        for(int j=0;j<CardsStudied[i];j++){
            therand=quantitylist[0][1];
            for(int k=2;k<=quantitylist[0][0];k++){
                if((BaseStructure[(quantitylist[0][k])][i][(provisoryArray[(quantitylist[0][k])])]*BaseStructure[(quantitylist[0][k])][realcards][1])<(BaseStructure[therand][i][(provisoryArray[therand])]*BaseStructure[therand][realcards][1])){
                    therand=quantitylist[0][k];
                }
            }
            DecodedList[i][j][0]=therand;
            DecodedList[i][j][1]=BaseStructure[therand][i][(provisoryArray[therand])];
            provisoryArray[therand]+=1;
        }
        free(provisoryArray);
    }
}
void PrintBest(int manysites,int realcards,int *CardsStudied,float ***DecodedList,int **quantitylist,float ***BaseStructure){
    FILE *reads= fopen("summarysites.txt","r");
    FILE *readc= fopen("summarycards.txt","r");
    char **SiteNames=malloc(manysites*sizeof(char*));
    char **CardNames=malloc(realcards*sizeof(char*));

    for(int i=0;i<realcards;i++) fscanf(readc,"%m[^\n] ",&(CardNames[i]));
    fclose(readc);
    for(int i=0;i<manysites;i++) fscanf(reads,"%m[^\n] ",&(SiteNames[i]));
    fclose(reads);

    for(int i=0;i<realcards;i++){
        for(int j=0;j<CardsStudied[i];j++) printf("%s No. %d in %s: R$ %0.2f\n",CardNames[i],(j+1),SiteNames[((int)(DecodedList[i][j][0]))],DecodedList[i][j][1]);
        printf("\n");
    }
    printf("\n");
    for(int i=1;i<=quantitylist[0][0];i++){
        printf("%s Shipping Cost: %0.2f\n",SiteNames[(quantitylist[0][i])],BaseStructure[(quantitylist[0][i])][realcards][0]);
        printf("%s Insurance Cost %d%%\n\n",SiteNames[(quantitylist[0][i])],(int)((BaseStructure[(quantitylist[0][i])][realcards][1]*100)-100));
    }
    printf("\n");

}


///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
void EvolutionaryAlgorithm(int mutationtax,int genocidetax,int manyparentals,int predationtax,double **Best){
    float ***DecodedList=NULL;
    float ***BaseStructure=NULL;
    float *Fitness=NULL;
    float *Fitness2=NULL;
    int **quantitylist=NULL;
    int **quantitylist2=NULL;
    int **siteslist=NULL;
    int **siteslist2=NULL;
    int *CardsStudied=NULL;
    float partial=0;
    int eval=0;
    int last=0;
    int realcards=0,manycards=0,manysites=0,mutation=1,occurences=0,total=0,repetitions=5000;
    float PreviousBest;
    clock_t begin = clock(),end;

    FILE *clearf= fopen("coordinates.txt","w");
    fclose(clearf);
    FILE *filem= fopen("coordinates.txt","a+");

    srand(time(NULL));

    manyparentals*=10;

    AppendFromTxt(&BaseStructure,&CardsStudied,&realcards,&manycards,&manysites);


    CreateAll(CardsStudied,&DecodedList,&Fitness,&Fitness2,&quantitylist,&quantitylist2,&siteslist,&siteslist2,manyparentals,manycards,manysites,realcards);
    ParentalGeneration(0,manysites,manyparentals,&Fitness,manycards,&quantitylist,&siteslist,BaseStructure,realcards,CardsStudied);
    FindBestWorst(Fitness,Fitness2,quantitylist,quantitylist2,siteslist,siteslist2,manyparentals,manycards,manysites,&last,0,1);
    PreviousBest=Fitness[0];

    printf("\n%f / %f\n",BaseStructure[0][realcards][0],BaseStructure[0][realcards][1]);
    printf("Good: %f\n",PreviousBest);

    eval=Evaluation(quantitylist,&PreviousBest,Fitness,&mutation,&occurences,manyparentals,0,mutationtax,genocidetax,&end);    

    for(int r=0;r<repetitions;r++){
        if((!r)&&(!(r%predationtax))) PredationGeneration(BaseStructure,&Fitness,&Fitness2,&quantitylist,&quantitylist2,&siteslist,&siteslist2,manysites,manyparentals,manycards,realcards,CardsStudied,&last);
        CrossoverGeneration(manysites,manyparentals,&Fitness,&siteslist2,&quantitylist2,manycards,&quantitylist,&siteslist,BaseStructure,realcards,&Fitness2,CardsStudied);
        MutationGeneration(manysites,manyparentals,&Fitness,mutation,manycards,&quantitylist,&siteslist,BaseStructure,realcards,CardsStudied);        
        FindBestWorst(Fitness,Fitness2,quantitylist,quantitylist2,siteslist,siteslist2,manyparentals,manycards,manysites,&last,(r+1),1);
        eval=Evaluation(quantitylist,&PreviousBest,Fitness,&mutation,&occurences,manyparentals,(r+1),mutationtax,genocidetax,&end);
        if(eval==2) ParentalGeneration(1,manysites,manyparentals,&Fitness,manycards,&quantitylist,&siteslist,BaseStructure,realcards,CardsStudied);
    }
    DecodeBestOnes(manysites,realcards,CardsStudied,quantitylist,BaseStructure,DecodedList);
    PrintBest(manysites,realcards,CardsStudied,DecodedList,quantitylist,BaseStructure);
    //PrintAll(manyparentals,quantitylist,Fitness,realcards,CardsStudied,BaseStructure,last);
    printf("%f\n",Fitness[0]);
    for(int i=1;i<=quantitylist[0][0];i++) printf("%d ",quantitylist[0][i]);
    (*Best)[0]=(double)Fitness[0];
    FreeForAll(&DecodedList,&BaseStructure,&Fitness,&Fitness2,&quantitylist,&quantitylist2,&siteslist,&siteslist2,&CardsStudied,manycards,realcards,manysites,manyparentals);
    (*Best)[1] = (double)(end - begin) / CLOCKS_PER_SEC;
}
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
int main(void){
    double *All=calloc(2,sizeof(float));
    EvolutionaryAlgorithm(10,10,10,5,&All);
    free(All);
    return 0;
}
