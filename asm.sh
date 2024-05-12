TARGET=the_byg_dotz
KICKASS=../../KickAss.jar
EXOMIZER=../exomizer

python3 genmask.py
python3 gen_txt.py

java -jar ${KICKASS} ${TARGET}.asm -o ${TARGET}_temp.prg
${EXOMIZER} sfx 0x080d ${TARGET}_temp.prg -n -o ${TARGET}.prg
