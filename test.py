from werkzeug.security import generate_password_hash, check_password_hash


val = check_password_hash('pbkdf2:sha256:150000$xagwaZzl$c7dcc3b9ec83a7e90737e0836e00fb87a7d05304d4939072d8800783dea80287', 'cheese0!')

val2 = generate_password_hash('queso0!')
#print(val2)

val3 =check_password_hash('pbkdf2:sha256:150000$LAX8sarZ$24dbdc3618380f4e592bbe8fb19764625afcba94058bba2c5bda7da4ac15aeb6', 'queso0!')

val4 = generate_password_hash('testing0!')

val5 =check_password_hash('pbkdf2:sha256:150000$u0Jznmwh$5489d9f5151149c97a00b7143889759ca8d5e8f2874a04148eb6db89e6402881', 'testing0!')
print(val5)

