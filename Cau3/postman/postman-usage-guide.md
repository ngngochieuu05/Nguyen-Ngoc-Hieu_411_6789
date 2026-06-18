# Huong dan dung Postman cho API Cipher

## 1. Chay Flask API

Mo terminal tai thu muc goc project:

```bash
cd lab_02/ex01_API
python api.py
```

Mac dinh server chay tai:

```text
http://127.0.0.1:5000/api
```

Neu port `5000` bi trung, doi port khi chay Flask va sua collection variable `base_url` trong Postman.

## 2. Import collection vao Postman

1. Mo Postman.
2. Bam `Import`.
3. Chon file collection da cap nhat:

```text
lab_02/ex01_API/postman/api-cipher-with-rsa.postman_collection.json
```

Neu ban van dung ten file cu thi co the import:

```text
lab_02/ex01_API/postman/api-cipher.postman_collection.json
```

4. Sau khi import se thay collection `API Cipher`.
5. Cau truc collection sau khi bo sung RSA va ECC:

```text
API Cipher
|-- Caesar
|   |-- POST Encrypt
|   |-- POST Decrypt
|   `-- POST Details / Matrix
|-- Vigenere
|   |-- POST Encrypt
|   |-- POST Decrypt
|   `-- POST Details / Matrix
|-- Playfair
|   |-- POST Encrypt
|   |-- POST Decrypt
|   `-- POST Details / Matrix
|-- Rail Fence
|   |-- POST Encrypt
|   |-- POST Decrypt
|   `-- POST Details / Matrix
|-- Transposition
|   |-- POST Encrypt
|   |-- POST Decrypt
|   `-- POST Details / Matrix
|-- RSA
|   |-- GET Generate Keys
|   |-- POST Encrypt
|   |-- POST Decrypt
|   |-- POST Sign
|   `-- POST Verify
`-- ECC
    |-- GET Generate Keys
    |-- POST Encrypt
    |-- POST Decrypt
    |-- POST Sign
    `-- POST Verify
```

## 3. Cach test nhanh cac cipher doi xung/co dien

Ap dung cho cac thuat toan:

- Caesar
- Vigenere
- Playfair
- Rail Fence
- Transposition

Cach test:

1. Chon request `Encrypt` cua thuat toan can test.
2. Bam `Send`.
3. Postman se tu luu ket qua ma hoa vao collection variable.
4. Chon request `Decrypt` cung folder.
5. Bam `Send` de giai ma lai.
6. Chon request `Details / Matrix`.
7. Bam `Send` de xem bang/ma tran/thong tin lien quan.

Vi du `Caesar/Encrypt`:

```json
{
  "plain_text": "Hello World",
  "key": "3"
}
```

Ket qua:

```json
{
  "action": "encrypt",
  "algorithm": "caesar",
  "encrypted_text": "Khoor Zruog",
  "result": "Khoor Zruog"
}
```

## 4. Cach test nhanh RSA

RSA co 5 request:

```text
RSA
|-- GET Generate Keys
|-- POST Encrypt
|-- POST Decrypt
|-- POST Sign
`-- POST Verify
```

Thu tu test nen lam nhu sau:

```text
1. RSA / Generate Keys
2. RSA / Encrypt
3. RSA / Decrypt
4. RSA / Sign
5. RSA / Verify
```

### 4.1. Generate Keys

Dung de tao cap khoa RSA gom public key va private key.

```text
GET {{base_url}}/rsa/generate_keys
```

Neu thanh cong, API tra ve:

```json
{
  "message": "Keys generated successfully"
}
```

Sau buoc nay, trong folder `key` se co 2 file khoa:

```text
publicKey.pem
privateKey.pem
```

### 4.2. Encrypt

Dung public key de ma hoa noi dung.

```text
POST {{base_url}}/rsa/encrypt
```

Body mau:

```json
{
  "message": "HUTECH University",
  "key_type": "public"
}
```

Ket qua tra ve co dang:

```json
{
  "encrypted_message": "..."
}
```

Trong Postman collection, request `RSA / Encrypt` da co script tu dong luu ket qua vao bien:

```text
rsa_ciphertext
```

### 4.3. Decrypt

Dung private key de giai ma noi dung da ma hoa.

```text
POST {{base_url}}/rsa/decrypt
```

Body mau:

```json
{
  "ciphertext": "{{rsa_ciphertext}}",
  "key_type": "private"
}
```

Ket qua mong muon:

```json
{
  "decrypted_message": "HUTECH University"
}
```

### 4.4. Sign

Dung private key de ky chu ky so cho message.

```text
POST {{base_url}}/rsa/sign
```

Body mau:

```json
{
  "message": "HUTECH University"
}
```

Ket qua tra ve co dang:

```json
{
  "signature": "..."
}
```

Trong Postman collection, request `RSA / Sign` da co script tu dong luu ket qua vao bien:

```text
rsa_signature
```

### 4.5. Verify

Dung public key de kiem tra chu ky so.

```text
POST {{base_url}}/rsa/verify
```

Body mau:

```json
{
  "message": "HUTECH University",
  "signature": "{{rsa_signature}}"
}
```

Neu chu ky hop le, ket qua tra ve:

```json
{
  "is_verified": true
}
```

Neu message bi thay doi hoac signature sai, ket qua co the la:

```json
{
  "is_verified": false
}
```

## 4a. Cach test nhanh ECC

ECC co 5 request tuong tu RSA:

```text
ECC
|-- GET Generate Keys
|-- POST Encrypt
|-- POST Decrypt
|-- POST Sign
`-- POST Verify
```

Thu tu test:

```text
1. ECC / Generate Keys
2. ECC / Encrypt
3. ECC / Decrypt
4. ECC / Sign
5. ECC / Verify
```

### 4a.1. Generate Keys
Tao cap khoa ECC (private_key.json va public_key.json).
```text
GET {{base_url}}/ecc/generate_keys
```

### 4a.2. Encrypt
Mã hóa dùng public key.
```text
POST {{base_url}}/ecc/encrypt
```
Body mau:
```json
{
  "message": "HUtech"
}
```
Ket qua tra ve chua `encrypted_message` (Base64) se duoc tu dong luu vao bien `ecc_ciphertext`.

### 4a.3. Decrypt
Giai ma dung private key.
```text
POST {{base_url}}/ecc/decrypt
```
Body mau:
```json
{
  "ciphertext": "{{ecc_ciphertext}}"
}
```

### 4a.4. Sign
Ky chu ky so bang private key.
```text
POST {{base_url}}/ecc/sign
```
Body mau:
```json
{
  "message": "HUtech"
}
```
Ket qua tra ve chua `signature` (Hex) se duoc tu dong luu vao bien `ecc_signature`.

### 4a.5. Verify
Xac thuc chu ky so.
```text
POST {{base_url}}/ecc/verify
```
Body mau:
```json
{
  "message": "HUtech",
  "signature": "{{ecc_signature}}"
}
```

## 5. Xem ma tran trong Postman

Request `Details / Matrix` dung chung endpoint:

```text
POST /<algorithm>/details
```

Body mau:

```json
{
  "plain_text": "Hello World",
  "key": "KEY"
}
```

Ket qua nam trong field `details`.

| Thuat toan | Details tra ve |
|---|---|
| Caesar | `alphabet`, `shift`, `normalized_shift`, `mapping` |
| Vigenere | `matrix` tabula recta 26x26, `formatted_key`, `key_shifts`, `key_stream` |
| Playfair | `matrix` 5x5, `normalized_key`, `normalized_text`, `pairs`, `position_map`, `rules` |
| Rail Fence | `matrix` zigzag, `rail_count`, `pattern`, `rails` |
| Transposition | `matrix`, `key_row`, `column_order`, `ordered_columns`, `padded_text` |

Trong Postman, chon tab `Body` cua response va de che do `Pretty` + `JSON` de nhin ma tran ro hon.

Luu y: RSA khong co request `Details / Matrix` vi RSA khong dung bang chu cai/ma tran nhu cac thuat toan co dien.

## 6. Danh sach endpoint

### 6.1. Cipher co dien

| Thuat toan | Encrypt | Decrypt | Details |
|---|---|---|---|
| Caesar | `POST /caesar/encrypt` | `POST /caesar/decrypt` | `POST /caesar/details` |
| Vigenere | `POST /vigenere/encrypt` | `POST /vigenere/decrypt` | `POST /vigenere/details` |
| Playfair | `POST /playfair/encrypt` | `POST /playfair/decrypt` | `POST /playfair/details` |
| Rail Fence | `POST /railfence/encrypt` | `POST /railfence/decrypt` | `POST /railfence/details` |
| Transposition | `POST /transposition/encrypt` | `POST /transposition/decrypt` | `POST /transposition/details` |

### 6.2. RSA va ECC

| Thuat toan | Chuc nang | Method | Endpoint |
|---|---|---:|---|
| **RSA** | Tao khoa | GET | `/rsa/generate_keys` |
| | Ma hoa | POST | `/rsa/encrypt` |
| | Giai ma | POST | `/rsa/decrypt` |
| | Ky chu ky so | POST | `/rsa/sign` |
| | Xac thuc chu ky so | POST | `/rsa/verify` |
| **ECC** | Tao khoa | GET | `/ecc/generate_keys` |
| | Ma hoa | POST | `/ecc/encrypt` |
| | Giai ma | POST | `/ecc/decrypt` |
| | Ky chu ky so | POST | `/ecc/sign` |
| | Xac thuc chu ky so | POST | `/ecc/verify` |

## 7. Body mau

### 7.1. Body mau cho cipher co dien

Encrypt:

```json
{
  "plain_text": "Hello World",
  "key": "KEY"
}
```

Decrypt:

```json
{
  "encrypted_text": "Rijvs Uyvjn",
  "key": "KEY"
}
```

Details:

```json
{
  "plain_text": "Hello World",
  "key": "KEY"
}
```

### 7.2. Body mau cho RSA

Generate Keys khong can body.

Encrypt:

```json
{
  "message": "HUTECH University",
  "key_type": "public"
}
```

Decrypt:

```json
{
  "ciphertext": "{{rsa_ciphertext}}",
  "key_type": "private"
}
```

Sign:

```json
{
  "message": "HUTECH University"
}
```

Verify:

```json
{
  "message": "HUTECH University",
  "signature": "{{rsa_signature}}"
}
```

### 7.3. Body mau cho ECC

Generate Keys khong can body.

Encrypt:
```json
{
  "message": "HUtech"
}
```

Decrypt:
```json
{
  "ciphertext": "{{ecc_ciphertext}}"
}
```

Sign:
```json
{
  "message": "HUtech"
}
```

Verify:
```json
{
  "message": "HUtech",
  "signature": "{{ecc_signature}}"
}
```

## 8. Collection Variables

Collection dang su dung cac bien sau:

| Bien | Cong dung |
|---|---|
| `base_url` | Dia chi goc cua API, mac dinh `http://127.0.0.1:5000/api` |
| `caesar_cipher_text` | Luu ket qua ma hoa Caesar |
| `vigenere_cipher_text` | Luu ket qua ma hoa Vigenere |
| `playfair_cipher_text` | Luu ket qua ma hoa Playfair |
| `railfence_cipher_text` | Luu ket qua ma hoa Rail Fence |
| `transposition_cipher_text` | Luu ket qua ma hoa Transposition |
| `rsa_ciphertext` | Luu ket qua ma hoa RSA |
| `rsa_signature` | Luu chu ky so RSA |
| `ecc_ciphertext` | Luu ket qua ma hoa ECC |
| `ecc_signature` | Luu chu ky so ECC |

Neu doi host/port, vao collection `API Cipher` -> `Variables` -> sua `base_url`.

## 9. Luu y

- `Caesar` va `Rail Fence` dung key dang so.
- `Vigenere`, `Playfair`, `Transposition` dung key dang chuoi.
- `Playfair` chuyen chuoi ve chu hoa, bo khoang trang, doi `J` thanh `I`.
- `Transposition` tu them ky tu dem `X` khi do dai chuoi khong chia het cho do dai key.
- Ca RSA va ECC can chay `Generate Keys` truoc khi `Encrypt`, `Decrypt`, `Sign`, `Verify`.
- RSA ma hoa bang `public key` va giai ma bang `private key`, luu o dang file `.pem` trong folder `keys`.
- ECC luu cap khoa trong file JSON (`private_key.json` va `public_key.json`) trong folder `keys` tuong ung.
- ECC su dung cac gia tri ngau nhien (nonce) trong qua trinh ma hoa va ky so, nen moi lan chay se sinh ra ciphertext va signature khac nhau (nhung van decrypt va verify hop le).
- Neu request bi loi do khong tim thay file key, hãy kiem tra folder keys cua thuat toan xem da duoc tao chua.
