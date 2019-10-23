loadI 1024 => r0
loadI 1028 => r1
load r0 => r0
load r1 => r1
add r0, r1 => r3
add r3, r1 => r4
loadI 1032 => r8
store r4 => r9
add r4, r4 => r5 // tests ability to handle use of same registers
loadI 1036 => r6
store r5 => r6
output 1024
output 1028
output 1032
output 1036
lshift r4,r4 => r30
loadI 1044 => r50
store r30 => r50
output 1044
rshift r30,r4 => r20
loadI 1040 => r17
store r20 => r17
output 1040