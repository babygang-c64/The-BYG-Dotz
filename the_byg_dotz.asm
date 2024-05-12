//========================================================================
// The BYG dotz, released at X party 2024, May 11th 2024
//
// vic bank : $4000-7fff
// screen : 4000-4400
// hires : 6000+
// sprites : 4400 OK
// ram dispo : 8b00+
//
// Music by Magnar, GFX by Nyke, Code by Papapower
//========================================================================

.label save_y = $50
.label zp_anim = save_y + 1
.label zp_dest = zp_anim + 2
.label zp_data = zp_dest + 2
.label zp_sprites = zp_data + 2 
.label zp_dest_sprites = zp_sprites + 2 
.label save_spr = zp_dest_sprites + 2
.label data_sprites = $8b00


* = 2061   "intro code"
intro_code:
    sei
    lda #%00111111
    sta $d015
    sta $d017
    sta $d01d
    ldx #15
setup_positions:
    lda positions,x
    sta $d000,x
    dex
    bpl setup_positions

    ldx #7
    lda #11
setup_colors:
    sta $d027,x
    dex
    bpl setup_colors

    lda #32
    sta $d010

    lda #0
    jsr $1000
    lda #$35
    sta $01

    jsr save_xy

    setup_raster_irq(raster, 248)
    cli

loop:
    jmp loop

positions:
    .byte $28,$fc,$58,$fc,$88,$fc,$b8,$fc
    .byte $e8,$fc,$18,$fc,$00,$00,$00,$00

// init

init:
    ldx #0
    stx $d020
    stx $d021
    lda #$3b
    sta $d011
    lda #$d8
    sta $d016
    lda #$02
    sta $dd00
    lda #$08
    sta $d018

    // copy coulors and clear sprites data 4400 to 4580
copie_couleur:
    lda $6000+8000,x
    sta $4000,x
    lda $6100+8000,x
    sta $4100,x
    lda $6200+8000,x
    sta $4200,x
    lda $6300+8000,x
    sta $4300,x
    lda $6000+9000,x
    sta $d800,x
    lda $6100+9000,x
    sta $d900,x
    lda $6200+9000,x
    sta $da00,x
    lda $6300+9000,x
    sta $db00,x
    lda #0
    sta $4400,x
    sta $4500,x
    inx
    bne copie_couleur

    ldy #1024/64
    ldx #0
init_data_sprites:
    tya
    sta $4400-8,x
    iny
    inx
    cpx #8
    bne init_data_sprites

    lda #<anim_frames_list
    sta zp_data
    lda #>anim_frames_list
    sta zp_data+1

    jmp reset_data_sprites

//----------------------------------------------------------------------------
// plot_sprites : value from zp $50 / $ 51
//----------------------------------------------------------------------------

plot_sprites:
    ldy #0
    lda (zp_sprites),y
    cmp #$ff
    beq test_reset_data_sprites

    inc zp_sprites
    bne pas_inc_spr1
    inc zp_sprites+1
pas_inc_spr1:

    sta zp_dest_sprites
    lda (zp_sprites),y
    sta save_spr
    and #%00111111
    clc
    adc #$44
    sta zp_dest_sprites+1

    inc zp_sprites
    bne pas_inc_spr2
    inc zp_sprites+1
pas_inc_spr2:

    lda save_spr
    and #%11000000
    clc
    rol
    rol
    rol
    tax
    lda mask_x,x
    sta save_spr

    lda (zp_dest_sprites),y
    eor save_spr
    sta (zp_dest_sprites),y
    ldy #3
    sta (zp_dest_sprites),y
    clc
    rts

mask_x:
    .byte %11000000, %00110000, %00001100, %00000011

test_reset_data_sprites:
    inc zp_sprites
    bne pas_inc3
    inc zp_sprites+1
pas_inc3:

    lda (zp_sprites),y
    cmp #255
    beq reset_data_sprites
    sta scroll_pause

    inc zp_sprites
    bne pas_inc4
    inc zp_sprites+1
pas_inc4:

    sec
    rts

reset_data_sprites:
    ldy #0
    lda #<data_sprites
    sta zp_sprites
    lda #>data_sprites
    sta zp_sprites+1
    clc
    rts

//----------------------------------------------------------------------------
// save and restore y = 24, x = 16,20 and y = 14, x = 31,32
//----------------------------------------------------------------------------

save_xy:
    ldx #7
do_save:
    lda $6000+320*24+16*8,x
    sta save1,x
    lda $6000+320*24+20*8,x
    sta save2,x
    dex
    bpl do_save
    rts

restore_xy:
    ldx #7
do_restore:
    lda save1,x
    sta $6000+320*24+16*8,x
    lda save2,x
    sta $6000+320*24+20*8,x
    lda save3,x
    sta $6000+320*14+31*8,x
    lda save4,x
    sta $6000+320*14+32*8,x
    dex
    bpl do_restore
    rts

//----------------------------------------------------------------------------
// plot_frame : draws frame X
//----------------------------------------------------------------------------

plot_frame:
{
    lda frames_l,x
    sta zp_anim
    lda frames_h,x
    sta zp_anim+1
    ldy #0
    lda (zp_anim),y
anim_loop:
    tax
    getNextByte(zp_anim)
    sta zp_dest
    getNextByte(zp_anim)
    sta zp_dest+1
    sty save_y
    ldy #0

    lda bitmask,x
    sta (zp_dest),y
    iny
    sta (zp_dest),y
    iny
    sta (zp_dest),y
    iny
    sta (zp_dest),y
    inx
    iny
    lda bitmask,x
    sta (zp_dest),y
    iny
    sta (zp_dest),y
    iny
    sta (zp_dest),y
    iny
    sta (zp_dest),y

    ldy save_y
    getNextByte(zp_anim)
    beq fin_anim
    bne anim_loop
fin_anim:
    rts
}

//----------------------------------------------------------------------------
// raster code
//----------------------------------------------------------------------------

raster:
    save_reg_irq()

    lda step
    beq pas_suite
    jmp suite
pas_suite:

    ldx petscii_posH
    ldy petscii_posL
    lda petscii,y
.for (var posY=0;posY<25;posY++) {
        sta $0400+40*posY,x
    }
    lda #14
.for (var posY=0;posY<25;posY++) {
        sta $d800+40*posY,x
    }
    inc petscii_posL
    lda petscii_posL
    cmp #5
    beq ok_raster
    jmp fin_raster
ok_raster:
    lda #0
    sta petscii_posL
    inc petscii_posH
    lda petscii_posH
    cmp #40
    bne fin_raster
    inc step
    jsr init
    jmp fin_raster

suite:

    // open borders

    lda $d012
w249:
    cmp $d012
    beq w249

    lda $d011
    and #$f7
    sta $d011

    lda #$ff
w255:
    cmp $d012
    bne w255

    lda $d011
    ora #8
    sta $d011

    // play music first
    jsr $1003

    // then animate sprites
    jsr do_plot_sprites
    lda delay
    beq redo
    dec delay
    jmp fin_raster

do_plot_sprites:
    lda scroll_pause
    beq ok_plot
    dec scroll_pause
    rts

ok_plot:
    jsr plot_sprites
    bcc encore_sprite
    rts
encore_sprite:
    jmp plot_sprites

scroll_pause:
    .byte 0

redo:
    ldy #0
    lda (zp_data),y
    bpl anim_ok
    lda #<anim_frames_list
    sta zp_data
    lda #>anim_frames_list
    sta zp_data+1
    jmp redo

anim_ok:
    tax
    inc zp_data
    bne pas_inc
    inc zp_data+1
pas_inc:
    lda (zp_data),y
    sta delay
    inc zp_data
    bne pas_inc2
    inc zp_data+1
pas_inc2:
    jsr plot_frame

fin_raster:
    end_raster_irq()

frame:
    .byte 0

delay:
    .byte 0

.print "frame=$"+toHexString(frame)
.print "delay=$"+toHexString(delay)

save1:
    .byte 0,0,0,0,0,0,0,0
save2:
    .byte 0,0,0,0,0,0,0,0
save3:
    .byte $0f,$0f,$0f,$ff,$ff,$ff,$ff,$ff
save4:
    .byte $0f,$0f,$0f,$ff,$ff,$ff,$ff,$ff

petscii:
    .byte 116,117,97,246,160
petscii_posL:
    .byte 0
petscii_posH:
    .byte 0
step:
    .byte 0

//----------------------------------------------------------------------------
// macro getNextByte(zp)
//----------------------------------------------------------------------------

.macro getNextByte(zp) {
    iny
    bne pas_inc
    inc zp+1
pas_inc:
    lda (zp),y
}

//----------------------------------------------------------------------------
// setup_raster_irq
//
//	A,X : < and > irq address
// 	Y : raster line for irq
//----------------------------------------------------------------------------

.macro setup_raster_irq(adr, y)
{
	sei
	lda #<adr
	sta $fffe
	lda #>adr
	sta $ffff
	lda #y
	sta $d012

	//-- init IRQ
    lda #$7f
    sta $dc0d
    sta $dd0d
    and $d011
    sta $d011
    lda #1      // enable raster IRQ
    sta $d01a
    lda $dc0d	// ack CIA-1
    lda $dd0d	// ack CIA-2
}

//----------------------------------------------------------------------------
// end_raster_irq
//----------------------------------------------------------------------------

.macro end_raster_irq()
{
	asl $d019
	pla
	tay
	pla
	tax
	pla
	rti
}

//----------------------------------------------------------------------------
// save_reg_irq
//----------------------------------------------------------------------------

.macro save_reg_irq()
{
	pha
	txa
	pha
	tya
	pha
}

// screen_mask : positions that can be changed on screen
//
// 128 = not touched (bit 7)
// 1 = xx   2 = x.  3 = x.  4 = .x  5 = .x  6 = ..  7 = ..  8 = x.
//     xx       .x      ..      ..      x.      x.      .x      xx

* = $1000 "music"

    .import binary "sid.bin"

    .align $100
screen_mask:
* = * "screen_mask"
    .import binary "anim.bin"

    .align $100
bitmask:
    .byte 0,0,0,0,0,0,0,0
    // 1 = X000
    .byte $0f,$ff,$0f,$0f,$ff,$ff,$ff,$ff
    // 2 = 0X00
    .byte $f0,$ff,$f0,$f0,$ff,$ff,$ff,$ff
    // 3 = XX00
    .byte $00,$ff,$00,$00,$ff,$ff,$ff,$ff
    // 4 = 00X0
    .byte $ff,$0f,$ff,$ff,$0f,$0f,$0f,$0f
    // 5 = X0X0
    .byte $0f,$0f,$0f,$0f,$0f,$0f,$0f,$0f
    // 6 = 0XX0
    .byte $f0,$0f,$f0,$f0,$0f,$0f,$0f,$0f
    // 7 = XXX0
    .byte $00,$0f,$00,$00,$0f,$0f,$0f,$0f
    // 8 = 000X
    .byte $ff,$f0,$ff,$ff,$f0,$f0,$f0,$f0
    // 9 = X00X
    .byte $0f,$f0,$0f,$0f,$f0,$f0,$f0,$f0
    // 10 = 0X0X
    .byte $f0,$f0,$f0,$f0,$f0,$f0,$f0,$f0
    // 11 = XX0X
    .byte $00,$f0,$00,$00,$f0,$f0,$f0,$f0
    // 12 = 00XX
    .byte $ff,$00,$ff,$ff,$00,$00,$00,$00
    // 13 = X0XX
    .byte $0f,$00,$0f,$0f,$00,$00,$00,$00
    // 14 = 0XXX
    .byte $f0,$00,$f0,$f0,$00,$00,$00,$00
    // 15 = XXXX
    .byte $00,$00,$00,$00,$00,$00,$00,$00
    // 16 = 0000
    .byte $ff,$ff,$ff,$ff,$ff,$ff,$ff,$ff
* = $6000   "koala pic"
    .import c64 "babygang-empty.kla"

* = *   "frames data"
.align $100
frames_l:
    .import binary "framesL.bin"
.align $100
frames_h:
    .import binary "framesH.bin"

anim_frames_list:
    .import binary "anim_frames.bin"

* = data_sprites
    .import binary "flux.bin"
