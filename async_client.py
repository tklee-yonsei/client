import asyncio
import aiohttp

# 서버 URL 설정
ENCODE_API_URL = "http://localhost:6002/encode/qpsk"  # QPSK 인코딩 API
ADD_NOISE_API_URL = "http://localhost:6003/add_noise/gaussian"  # Gaussian 노이즈 추가 API
DECODE_API_URL = "http://localhost:6002/decode/qpsk"  # QPSK 디코딩 API

# 샘플 입력 신호
signal = [1, 0, 1, 1]
modulation_order = 4  # QPSK는 4차 변조 방식

async def qpsk_processing():
    async with aiohttp.ClientSession() as session:
        # Step 1: QPSK 인코딩
        print("Step 1: QPSK 인코딩")
        encode_payload = {
            "signal": signal,
            "modulation_order": modulation_order
        }
        
        async with session.post(ENCODE_API_URL, json=encode_payload) as response:
            encoded_signal = await response.json()
            encoded_signal = encoded_signal.get("encoded_signal")
            print(f"Encoded Signal: {encoded_signal}")

        # Step 2: Gaussian 노이즈 추가
        print("\nStep 2: Gaussian 노이즈 추가")
        noise_payload = {
            "encoded_signal": encoded_signal,
            "noise_level": 0.1  # Gaussian 노이즈 레벨 설정
        }

        async with session.post(ADD_NOISE_API_URL, json=noise_payload) as response:
            noisy_signal = await response.json()
            noisy_signal = noisy_signal.get("noisy_signal")
            print(f"Noisy Signal: {noisy_signal}")

        # Step 3: QPSK 디코딩
        print("\nStep 3: QPSK 디코딩")
        decode_payload = {
            "encoded_signal": noisy_signal,
            "modulation_order": modulation_order
        }

        async with session.post(DECODE_API_URL, json=decode_payload) as response:
            decoded_signal = await response.json()
            decoded_signal = decoded_signal.get("decoded_signal")
            print(f"Decoded Signal: {decoded_signal}")

# 비동기 함수 실행
asyncio.run(qpsk_processing())