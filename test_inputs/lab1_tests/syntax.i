// All valid syntax, should parse correctly

load  r1  => r2
loadI 27  => r1
store r2 => r4
add   r1,r2 => r3
sub   r3, r4 => r5
mult  r5, r6 => r10
lshift  r0, r3 => r2
rshift  r2, r3 => r2
output 1024
nop
loadI 27  => r1
loadI 27=>r1
load  r1 => r2
load  r1 => r2//a comment without whitespace
load  r1 =>r2 //a comment with whitespace
store r2 => r4
add   r1,r2 => r3
sub   r3, r4 => r5
mult  r5, r6 => r10
lshift  r0, r3 => r2
rshift  r2, r3 => r2
output 1024
