
# Chapter 03 학습 기록

## POST /members Contract

### Request Body
- name: string, required
- email: string, required
- age: integer, required

### Success
- 201 Created
- created member JSON

### Failure
- invalid body → 422
