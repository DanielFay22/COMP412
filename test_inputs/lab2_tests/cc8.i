loadI 1024 => r0
loadI 1032 => r1
loadI 1036 => r5
loadI 1036 => r6
loadI 1036 => r7
loadI 1036 => r8
store r5 => r5
store r6 => r6
store r7 => r7
store r8 => r8
store r0 => r0
store r1 => r1
add r0, r1 => r2
load r1 => r3
load r1 => r4
sub r0, r2 => r4
add r0, r2 => r3
mult r2, r2 => r3
store r2 => r2
store r5 => r5
store r6 => r6
store r7 => r7
store r8 => r8
output 1024
output 1032
output 1036
output 2056