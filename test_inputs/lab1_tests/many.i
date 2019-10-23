// cc3.i: block for the lab 2 code check
//        has multiple regions of 'high' demand
// Fall 2016, COMP 412, Rice University
//SIM INPUT -i 0 2 4
//OUTPUT: 50
loadI 0	        => r100
add   r100,r100	=> r0
loadI 4		=> r1
load  r0	=> r10
add   r0,r1	=> r2
load  r2	=> r11
add   r2,r1	=> r3
load  r3	=> r12
//
add   r10,r11	=> r10
add   r12,r11	=> r12
add   r10,r12   => r10
add   r10,r12   => r15
store r15	=> r0
//
load  r2	=> r11
add   r10,r11	=> r10
add   r12,r11	=> r12
add   r10,r12   => r10
add   r10,r12   => r15
store r15	=> r0
//
load  r2	=> r11
add   r10,r11	=> r10
add   r12,r11	=> r12
add   r10,r12   => r10
add   r10,r12   => r15
store r15	=> r0
//
store r15       => r100
output 0
