loadI 1024 => r0
loadI 0 => r1
store r0 => r1
load r1 => r0
loadI 1028 => r1
sub r0,r1 => r1
mult r1,r1 => r1
add r1,r0 => r3
lshift r0,r1 => r4
rshift r1,r4 => r1
store r1 => r0
output 1024