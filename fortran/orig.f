
      PROGRAM TRAPEZNO_KRILO

C     ******************************************************************
C                 PROGRAM RACUNA AERODINAMICKE KARAKTERISTIKE
C                        TRAPEZNOG VITOPERENOG KRILA
C      PRI ZADATOM KOEFICIJENTU UZGONA ILI NA ZADATOM REZIMU KRSTARENJA
C     ******************************************************************
C     Izvorna verzija programa (Glauert - jednostavna verzija sa konsta-
C     ntnim aeroprofilom i gradijentom uzgona 2PI, 8 preseka):
C       A. Kuethe, Univ. of Michigan & C. Chow, Univ. of Colorado, 1986.
C
C     Modifikovana verzija (zadavanje Cz, 16 preseka, realni aeroprofili
C     u korenu i na kraju, odredjivanje Czmx krila, opterecenja, itd.):
C          I. Kostic, MF Beograd, "Primenjena aerodinamika", 2008.

      DIMENSION A(16),ALAPS(16),ALIND(16),CXIND(16),CZL(16),
     &  CZ1(16),CZ2(16),CA(16),CB(16),COSTH(16),SINTH(16),
     &  D(16,16),TETA(16),Y(16),CZMAXAP(16),CZZMAX(16),CZLOKMAX(16),
     &  AAP(16),P(16),PMAX(16),ALOK(16)
      REAL LAM,LS,L(16)
      CHARACTER T
      T=CHAR(9) ! definise karakter TAB za laksi prenos izlaza u Excel

C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

      IZB=1
      DATA CZ / 0.200 /  !ZADATI KOEFICIJENT UZGONA KRILA
      DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
C                                          konst.
C              broj    vitkost suzenje   vitop.   brzina   gustina
C            preseka                     [step.]  [km/h]   [kg/m^3]
      DATA      K,       LAM,   EN,       EPS_K,    V,        RO
     &     /    16,      53.33,   0.500,      0.0,    50.00,    0.050000 /

      DATA CZMAXAP_S / 1.620 / ! maks. koef. uzgona ap. u korenu krila
      DATA CZMAXAP_0 / 1.46 / ! maks. koef. uzgona ap. na kraju krila
      DATA AAAP_S / 0.100 / !grad. uzgona ap. u korenu [1/o]
      DATA AAAP_0 / 0.110 / !grad. uzgona ap. na kraju [1/o]
      !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
      DATA ANAP_S / -1.2 / !ugao nultog uzgona ap. u korenu krila [o]
      DATA ANAP_0 / -1.0 / !ugao nultog uzgona ap. na kraju krila [o]
      DATA LS / 2.583 /  ! duzina tetive u korenu krila u metrima

C     ******************** KRAJ UNOSA PODATAKA *************************

      OPEN(2,FILE='IZLAZ.TXT',STATUS='UNKNOWN')

      PI=4.*ATAN(1.)

      AAP_S=AAAP_S*180./PI !pretvara gradijente uzgona osnovnih
      AAP_0=AAAP_0*180./PI !aeroprofila u vrednosti po radijanu
      EPS_A=ANAP_S-ANAP_0  !racuna aerodinamicko vitoperenje [o]
      VITOP=EPS_K+EPS_A  !racuna ukupno vitoperenje krila  [o]

C     ZA K RAVNOMERNO UGAONO RASPOREDJENIH INTERVALA U DOMENU 0 DO PI/2:

      CZNAP=CZMAXAP_0/CZMAXAP_S
      AAPN=AAP_0/AAP_S
      DO 5 J=1,K
         TETA(J)=PI*J/(2.*K)  !racuna vrednosti ugla Teta po razmahu
         COSTH(J)=COS(TETA(J))
         SINTH(J)=SIN(TETA(J))
         Y(J)=COSTH(J)  !racuna relativne preseke y/(b/2) po razmahu
      L(J)=1.-(1.-EN)*COSTH(J) !lokalna relativna tetiva Lj/LS
      AAP(J)=AAP_S*(1.-(1.-AAPN)*COSTH(J)) !lokalni grad. uzgona ap.
    5 CZMAXAP(J)=CZMAXAP_S*(1.-(1.-CZNAP)*COSTH(J)) !lok. max Cz. ap.

C     RACUNA FAKTORE D(J,N) KOJIMA SE MNOZE FURIJEOVI KOEF. U JED.(8.5):

      DO 10 J=1,K
         D1=1./L(J)*(AAP_S/AAP(J))
         D2=0.5*AAP_S/(LAM*(1.+EN)*SINTH(J))
            DO 10 N = 1,K
            I=2*N-1
   10 D(J,N)=(D1+D2*I)*SIN(I*TETA(J))

C     ZADAJU SE DVE VREDNOSTI, NPR. AL1=5.7...  I AL2=8.7... STEPENI
C     KAO NOMINALNI AERODINAMICKI NAPADNI UGLOVI U KORENU KRILA;
C     ZA AL1 RACUNA AERODINAMICKE NAPADNE UGLOVE PO RAZMAHU
C     (U RADIJANIMA) ZA IZABRANE POLOZAJE PO RAZMAHU I RESAVA JEDNACINE
C     (8.5) KORISCENJEM KRAMEROVOG PRAVILA. ZATIM RACUNA KOEFICIJENT
C     UZGONA KRILA CZK1 I LOKALNE AEROPROFILSKE KOEFICIJENTE UZGONA
C     CZ1(J) POMOCU IZRAZA IZVEDENIH IZ (5.10) I (5.6).
C     POTOM RACUNA KOEFICIJENTE BAZNE I ADITIVNE RASPODELE UZGONA
      DATA AL1, AL2 /5.76543, 8.76543/ !Ovo se ne dira!
      
      DO 15 J=1,K
   15 ALAPS(J)=(AL1+VITOP*COSTH(J))*PI/180.
      CALL CRAMER(D,ALAPS,A,K)
      CZK1=PI**2*A(1)/(1.+EN)*(AAP_S/(2*PI))
      DO 25 J=1,K
         SUM=0.0
            DO 20 N=1,K
   20       SUM=SUM+A(N)*SIN((2*N-1)*TETA(J))
         CZ1(J)=AAP_S/L(J)*SUM
   25 CONTINUE
   
C     ZA AL2 PONAVLJA SE ISTI POSTUPAK
      DO 30 J=1,K
   30 ALAPS(J)=(AL2+VITOP*COSTH(J))*PI/180
      CALL CRAMER(D,ALAPS,A,K)
      CZK2=PI**2*A(1)/(1.+EN)*(AAP_S/(2*PI))
      DO 40 J=1,K
         SUM=0.0
            DO 35 N=1,K
   35       SUM=SUM+A(N)*SIN((2*N-1)*TETA(J))
         CZ2(J)=AAP_S/L(J)*SUM
   40 CONTINUE

C     RESAVA JEDNACINE (8.6) PO CA(J) I CB(J), J = 1,2,...K
      DO 45 J=1,K
         CA(J)=(CZ2(J)-CZ1(J))/(CZK2-CZK1)
         CB(J)=CZ1(J)-CA(J)*CZK1
   45 CONTINUE

      WRITE(2,50)
      WRITE(*,50)
   50 FORMAT(///4X,'DEFINISANJE LOKALNIH PRESEKA TRAPEZNOG KRILA ',
     &  'I FAKTORA RASPODELE UZGONA'//
     &  13X,'presek   relativni    relativna   faktor    faktor'/
     &  13X,'  br.     razmah       tetiva      bazne   aditivne'/
     &  13X,'   j     y(j)/(b/2)    L(j)/Ls     Cb(j)    Ca(j)'/)
      WRITE(2,55) (J,Y(J),L(J),CB(J),CA(J), J=K,1,-1)
      WRITE(*,55) (J,Y(J),L(J),CB(J),CA(J), J=K,1,-1)
   55 FORMAT(16(15X,I2,F12.3,F12.3,F12.4,F9.4/))

C     SADA RACUNA AERODINAMICKE KARAKTERISTIKE KRILA ZA ZADATI
C     KOEFICIJENT UZGONA ILI REZIM LETA
      IF (IZB.EQ.1) THEN
          CZKK=CZ
          GO TO 61
      ELSE
          CZKK=SPECOP/(0.5*RO*(V/3.6)**2.)
      END IF
      WRITE(2,60)V,RO,SPECOP
      WRITE(*,60)V,RO,SPECOP
   60 FORMAT( ///8X,
     &'PRORACUN TRAPEZNOG KRILA ZA SLUCAJ LETA DEFINISANOG PARAMETRIMA:'
     &  //2X,'V = ',F6.1,' [km/h], Ro =',F7.4, ' [kg/m^3],',
     &  ' spec. opt. krila = ',F6.1,' [N/m^2]')
      GO TO 63
   61 WRITE(2,62)V,RO,CZKK
      WRITE(*,62)V,RO,CZKK
   62 FORMAT( ///8X,
     &'PRORACUN TRAPEZNOG KRILA ZA SLUCAJ LETA DEFINISANOG PARAMETRIMA:'
     &  //2X,'V = ',F6.1,' [km/h], Ro =',F7.4, ' [kg/m^3],',
     &  ' koeficijent uzgona krila CZ = ',F5.3)
     
C     AERODINAMICKI NAPADNI UGAO U KORENU KOJI CE ODGOVARATI OVOM CZKK
C     ODREDJUJE SE IZ PROPORCIJE:
   63 ALF=AL1+(AL2-AL1)*(CZKK-CZK1)/(CZK2-CZK1)
      
C     LOKALNI KOEFICIJENTI UZGONA PO RAZMAHU MOGU SE RACUNATI POMOCU
C     JEDNACINE (6.6), ILI KORISCENJEM  JEDNACINE(5.6). U CILJU PROVERE
C     UKUPNE TCANOSTI PRORACUNA, RACUNAJU SE NA OBA NACINA.
C     PRVO SE KORISTI KORISTI IZRAZ (6.6):
      DO 65 J=1,K
   65 CZL(J)=CB(J)+CA(J)*CZKK

      WRITE(2,70) (CZL(J),J=K,1,-1)
      WRITE(*,70) (CZL(J),J=K,1,-1)
   70 FORMAT(//4X,'POREDJENJE LOKALNIH KOEFICIJENATA UZGONA',
     &' DOBIJENIH NA DVA NACINA:'/
     &  4X,'(od korena prema kraju krila, j = 16,15,...1)'//
     &  6X,'Ovi su dobijeni na osnovu jednacine (6.6):'/5X,8F9.5/
     &  5X,8F9.5/)

C     SADA SE KORISTI JEDNACINA (5.6):
      DO 75 J=1,K
   75 ALAPS(J)=(ALF+VITOP*COSTH(J))*PI/180.
      CALL CRAMER(D,ALAPS,A,K)
      DO 85 J=1,K
         SUM=0.0
            DO 80 N=1,K
   80       SUM=SUM+A(N)*SIN((2*N-1)*TETA(J))
   85 CZL(J)=AAP_S/L(J)*SUM

      WRITE(2,90) (CZL(J),J=K,1,-1)
      WRITE(*,90) (CZL(J),J=K,1,-1)
   90 FORMAT(6X,'a ovi na osnovu jednacine (5.6):'/5X,8F9.5/
     & 5X,8F9.5/)

C     ZATIM SE RACUNAJU LOKALNI INDUKOVANI NAPADNI UGLOVI POMOCU
C     JEDNACINE (8.7), LOKALNI INDUKOVANI KOEFICIJENTI OTPORA POMOCU
C     (8.8), LOKALNO OPTERECENJE KRILA IZ (6.7), LOKALNI AEROPROFILSKI
C     GRADIJENT UZGONA KORISCENJEM (8.9).
C     UGLOVI SE PREVODE U STEPENE PRE STAMPANJA

      DO 100 J=1,K
         SUM=0.0
            DO 95 N=1,K
            I=2*N-1
   95       SUM=SUM+I*A(N)*SIN(I*TETA(J))/SINTH(J)
         ALIND(J)= 0.5*AAP_S/(LAM*(1+EN))*SUM
         CXIND(J)= CZL(J)*ALIND(J)
         ALOK(J)=CZL(J)/ALAPS(J)
         P(J)=CZL(J)*0.5*RO*(V/3.6)**2*L(J)*LS !lokalno opter. krila
  100 ALIND(J)=ALIND(J)*180./PI

      WRITE(2,104) (A(N), N=1,K)
      WRITE(*,104) (A(N), N=1,K)
  104 FORMAT(//6X,'KOEFICIJENTI FURIJEOVOG REDA',
     & ' A1,A3,A5,.....A31 SU:',/4X,8F9.4/4X,8F9.4/)
      WRITE(2,105) LAM,EN,EPS_K,VITOP,AAAP_S,AAAP_0,ANAP_S,ANAP_0,LS
      WRITE(*,105) LAM,EN,EPS_K,VITOP,AAAP_S,AAAP_0,ANAP_S,ANAP_0,LS
  105 FORMAT(//23X,'AERODINAMICKE KARAKTERISTIKE PO PRESECIMA KRILA'//
     &' ZA: VITKOST',F5.2,'; SUZENJE',F5.2,'; KONST. VITOP.',
     &F5.1,' [o].','; UKUPNO VITOP.',F5.1,' [o].'/
     &' Parametri osnovnih aeroprofila:'/
     &' a(S) =',F5.3,'[1/o]; a(0) =',F5.3,'[1/o]; AlfaN(S) =',
     & F4.1,' [o]; AlfaN(0) =',F4.1,' [o]',
     &';  Tetiva u korenu L(S) =',F6.3,' [m]'//)
      WRITE(2,106)
      WRITE(*,106)
  106 FORMAT(' j','      y(j)/(b/2)','  Cz lok','        a[1/rad]',
     & '         a[1/step]','       Alfa ind','         Cxi lok',
     & '         p [N/m]' )
      WRITE(2,107)(J,T,Y(J),T,CZL(J),T,ALOK(J),T,ALOK(J)/180.*PI,T,
     &ALIND(J),T,CXIND(J),T,P(J), J=K,1,-1)
      WRITE(*,107)(J,T,Y(J),T,CZL(J),T,ALOK(J),T,ALOK(J)/180.*PI,T,
     &ALIND(J),T,CXIND(J),T,P(J), J=K,1,-1)
  107 FORMAT(/16(1X,I2,A1,F7.3,A1,F9.3,A1,F8.3,A1,F10.4,A1,F9.3,A1,
     & F11.5,A1,F11.2/))

C     SADA SE SRACUNAVA KOEFICIJENT INDUKOVANOG OTPORA KRILA CXINDK,
C     OSREDNJENI GRADIJENT UZGONA KRILA AKR, I (ADITIVNI TJ. NOMINALNI)
C     AERODINAMICKI NAPADNI UGAO ALAK KRILA, KORISCENJEM JEDNACINA
C     (5.12), (8.10) I (8.11), RESPEKTIVNO

      SUM=0.0
      DO 110 N=1,K
  110 SUM=SUM+(2*N-1)*A(N)**2
      CXINDK=PI**3/(LAM*(1.+EN)**2)*SUM*(AAP_S/2/PI)**2

      SUM=0.0
      KM1=K-1
      DO 115 J=1,KM1
  115 SUM=SUM+(ALOK(J)*L(J)+ALOK(J+1)*L(J+1))*(Y(J)-Y(J+1))
      AKR=SUM/(1.+EN)
      ALAK=CZKK/AKR*180./PI
      
      ALFAG=ALF+ANAP_S !geometrijski napadni ugao celog krila
      ALFAN=ALFAG-ALAK !ugao nultog uzgona celog krila
      DEL=CXINDK/(CZKK**2/PI/LAM)-1. !popravni faktor ind. otp. "delta"
      WRITE(2,120) CZKK,CXINDK,DEL,AKR/180.*PI,ALAK,ALF,ALFAG,ALFAN
      WRITE(*,120) CZKK,CXINDK,DEL,AKR/180.*PI,ALAK,ALF,ALFAG,ALFAN
  120 FORMAT(/1X,'KARAKTERISTIKE KRILA PRI ZADATOM ',
     & 'KOEFICIJENTU UZGONA ILI REZIMU KRSTARENJA',//
     & 7X,'KOEFICIJENT UZGONA KRILA            Cz =',F6.3/
     & 7X,'KOEF. INDUKOVANOG OTPORA KRILA      Cxi =',F8.5/
     & 7X,'Popravni faktor indukovanog otpora  delta =',F8.5/
     & 7X,'GRADIJENT UZGONA KRILA              a =',F8.4,' [1/o]'/
     & 7X,'aerodinamicki napadni ugao krila    AlfaA =',F7.2,' [o]'/
     & 7X,'aerodinamicki nap. ugao u korenu    AlfaAs=',F7.2,' [o]'/
     & 7X,'GEOMETRIJSKI NAPADNI UGAO KRILA     Alfa  =',F7.2,' [o]'/
     & 7X,'UGAO NULTOG UZGONA KRILA            AlfaN =',F7.2,' [o]'//)

C     PRORACUN MAKSIMALNOG KOEFICIJENTA UZGONA KRILA CZMAX - MINIMALNA
C     VREDNOST FUNKCIJE (czmax-cb)/ca, KAO I PRORACUN LOKALNOG
C     KOEFICIJENTA UZGONA I OPTERECENJA PRI CZMAX

      DO 130 J=1,K
  130 CZZMAX(J)=(CZMAXAP(J)-CB(J))/CA(J) !(czmax-cb)/ca
      CZMAX=MIN(CZZMAX(1),CZZMAX(2),CZZMAX(3),CZZMAX(4),CZZMAX(5),
     &      CZZMAX(6),CZZMAX(7),CZZMAX(8),CZZMAX(9),CZZMAX(10),
     &      CZZMAX(11),CZZMAX(12),CZZMAX(13),CZZMAX(14),
     &      CZZMAX(15),CZZMAX(16)) !OVO SE RUCNO MENJA ZA BROJ PRESEKA!
      DO 131 J=1,K
         CZLOKMAX(J)=CA(J)*CZMAX+CB(J) !LOKANO cz pri Czmx KRILA
  131 PMAX(J)=CZLOKMAX(J)*0.5*RO*(V/3.6)**2*L(J)*LS!Opt. pri Czmx KRILA
  
      WRITE(2,134)
      WRITE(*,134)
  134 FORMAT('   y/(b/2)         Czmax ap.     (Czmax ap.-Cb)/Ca',
     &       '    Cz lok        Pmax [N/m]'/
     &       35X,'                pri CZmax krila'/)
  
      WRITE(2,135)(Y(J),T,CZMAXAP(J),T,CZZMAX(J),T,CZLOKMAX(J),T,PMAX(J)
     &, J=K,1,-1)
      WRITE(*,135)(Y(J),T,CZMAXAP(J),T,CZZMAX(J),T,CZLOKMAX(J),T,PMAX(J)
     &, J=K,1,-1)
  135 FORMAT(4X,F5.3,A1,F9.3,A1,F12.3,A1,F12.3,A1,F12.2)
      WRITE(2,136) CZMAX
      WRITE(*,136) CZMAX
  136 FORMAT(//4X,'Maksimalni koeficijent uzgona krila CZmax =',F6.3)

      STOP
      END

C     ******************************************************************
C           PODPROGRAMI ZA RESAVANJE SISTEMA ALGEBARSKIH JEDNACINA
C     ******************************************************************

      SUBROUTINE CRAMER(C,A,X,N)

C         OVAJ PODPROGRAM KORISTI SE ZA RESAVANJE SISTEMA ALGEBARSKIH
C         JEDNACINA TIPA:
C                    C(I,J)*X(J) = A(I)   I = 1,2,....N
C
C     NAPOMENA: DIMENZIJE U SLEDECOJ DEKLARACIJI MORAJU BITI JEDNAKE
C               BROJNOJ VREDNOSTI "N"

      DIMENSION C(16,16),CC(16,16),A(16),X(16)

      DENOM=DETERM(C,N)
      DO 3 K=1,N
         DO 1 I=1,N
           DO 1 J=1,N
    1      CC(I,J)=C(I,J)
         DO 2 I=1,N
    2    CC(I,K)=A(I)
    3 X(K)=DETERM(CC,N)/DENOM

      RETURN
      END
      
C     ************************************************

      FUNCTION DETERM(ARRAY,N)

C     PODPROGRAM SLUZI ZA RACUNANJE DETERMINANTE MATRICE NxN
C     NAPOMENA: DIMENZIJE U SLEDECOJ DEKLARACIJI MORAJU BITI JEDNAKE
C               BROJNOJ VREDNOSTI "N"

      DIMENSION ARRAY(16,16),A(16,16)
      
      DO 1 I=1,N
      DO 1 J=1,N
    1 A(I,J)=ARRAY(I,J)
      M=1
    2 K=M+1
           DO 3 I=K,N
           RATIO=A(I,M)/A(M,M)
           DO 3 J=K,N
    3      A(I,J)=A(I,J)-A(M,J)*RATIO
        IF (M.EQ.N-1) GO TO 4
        M=M+1
      GO TO 2
    4 DETERM=1.
      DO 5 L=1,N
    5 DETERM=DETERM*A(L,L)

      RETURN
      END

