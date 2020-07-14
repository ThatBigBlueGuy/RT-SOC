! usage: ./RT-SOC
! Real Time Catan, CMD Line Version ~FORTRAN Edition~

PROGRAM RT_SOC
IMPLICIT NONE
CHARACTER(20) :: season_names(4)
CHARACTER(1) :: tmp
INTEGER :: number_of_seasons,p,d,mp,roll,turn,season
LOGICAL :: season_on,season_unassigned=.TRUE.
REAL :: harvest

season_names = ['Summer, +1 Wheat','Fall, +1 Timber ','Winter, +1 Stone','Spring, +1 Sheep']
number_of_seasons = size(season_names)

WRITE(*,'(A)') '     ___                                      ________         '
WRITE(*,'(A)') '  __(   )__                ___            ___(        )___     '
WRITE(*,'(A)') ' (_________)              {___|          (___          ___)    '
WRITE(*,'(A)') '                         _____|_____         (________)        '
WRITE(*,'(A)') '       Real Time        )__   |   __)                          '
WRITE(*,'(A)') '   Settlers of Catan    )__   |   __)                          '
WRITE(*,'(A)') '   ~FORTRAN Edition~    )__   |   __)                          '
WRITE(*,'(A)') '                        )_____|_____)                          '
WRITE(*,'(A)') '                     |________|_________/|                     '
WRITE(*,'(A)') '_____________________|__________________/______________________'
WRITE(*,'(A)') '                   _________              ___                  '
WRITE(*,'(A)') '      ____                      ______              ______     '
WRITE(*,'(A)') '                                                               '
WRITE(*,'(A)') 'Enter the initial period of time (seconds) a turn will last at the beginning of the game'
READ(*,*) p
WRITE(*,'(A)') 'Enter the amount of time (seconds) the turn time will decrease per turn'
READ(*,*) d
WRITE(*,'(A)') 'The minimum amount of time a turn can last'
READ(*,*) mp
WRITE(*,'(A)') 'Enable seasons? Y/N'
READ(*,*) tmp
DO WHILE (season_unassigned)
	IF ((tmp.EQ.('Y')).OR.(tmp.EQ.('y'))) THEN
		season_on=.TRUE.
		season_unassigned=.FALSE.
	ELSE IF ((tmp.EQ.('N')).OR.(tmp.EQ.('n'))) THEN
		season_on=.FALSE.
		season_unassigned=.FALSE.
	ELSE
		WRITE(*,'(A)') 'Invalid input - Enable seasons? Y/N'
		READ(*,*) tmp
		CYCLE
	END IF
END DO
CALL RANDOM_SEED()
CALL RANDOM_NUMBER(harvest)
season=NINT(harvest*4)
turn=0
WRITE(*,'(A)') 'Game is starting in'
WRITE(*,'(A)') '5...'
CALL SLEEP(1)
WRITE(*,'(A)') '4...'
CALL SLEEP(1)
WRITE(*,'(A)') '3...'
CALL SLEEP(1)
WRITE(*,'(A)') '2...'
CALL SLEEP(1)
WRITE(*,'(A)') '1...'
CALL SLEEP(1)
DO WHILE(.NOT.season_unassigned)
	turn=turn+1
	CALL dice_roll(roll)
	WRITE(*,'(A)') '_____________________________________'
	WRITE(*,'(A,i5)') 'Turn: ',turn
	IF (season_on) WRITE(*,'(A)') season_names(season)
	WRITE(*,'(A,i5)') 'Roll: ',roll
	IF ((p-d*(turn-1)).GT.mp) THEN
		WRITE(*,'(A,i5)') 'Turn Duration: ',p-d*(turn-1)
		WRITE(*,'(A)') '_____________________________________'
		CALL SLEEP(p-d*(turn-1))
	ELSE
		WRITE(*,'(A,i5)') 'Turn Duration: ',mp
		WRITE(*,'(A)') '_____________________________________'
		CALL SLEEP(mp)
	END IF

	season=season+1
	IF (season.GT.number_of_seasons) season=1
END DO

END PROGRAM 

SUBROUTINE dice_roll(roll)
	INTEGER :: minimum,maximum,roll1,roll2,roll
	REAL :: die1,die2
	CALL RANDOM_NUMBER(die1)
	CALL RANDOM_NUMBER(die2)
	roll = NINT(die1*6+0.5)+NINT(die2*6+0.5)
END SUBROUTINE
