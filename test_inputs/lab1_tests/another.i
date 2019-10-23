// another kind of error, suggested by a student during office hours
loadI 20=>r1
load  r1=>r2
// extra register on the end, should be syntax error
mult  r1,r2 => r3 r4 
// extra odd character on the end, should be lexical error
// or both lexical and syntax error
mult  r1,r2 => r3 a  
store r3 => r1  // another operation that should parse correctly
output 20

