require("./env")
require("./encoder")

function get_encoder(publicKey, password) {
    var encrypt = new window.JSEncrypt();
    encrypt.setPublicKey(publicKey);
    return "__RSA__" + encrypt.encrypt(password)
}
function demo(){
    return "demo"
}
publicKey ="-----BEGIN PUBLIC KEY-----\n" +
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1OWi0JWNagnRhJIpkPWZZbcXwvsLJ9pziJb00SwmjPDKeYTzlLsbU24WDPZlDSlH/E0FteYlkJnCgIAtS31SAy5LVGaecHYn4lsEo/ioT5vZpY7HrDQ/IIUUZa3YJuM26gZNdLcr0gm0+4yR3fix+aUyM3GML5bwjSm4EThrXJ2Fd9l+WlYvWJ4f4hyfFM245P7S7F56JCxjJeZDsFlvB+Ex/0xms/osbqCTrSoZd7jc7CbZhUbUzqn71e8oVhC6/eq+yV9pBgRiTMaAxcWTh7VRnhGCHNUs3HrAUfmPz72DMM+EQAwNbnh8qM9R7b1tW0KqYx0AKoEAFZ96xSpsNwIDAQAB\n" +
    "-----END PUBLIC KEY-----"
password = "123456"
console.log(get_encoder(publicKey,password))