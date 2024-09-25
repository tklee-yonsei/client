import asyncio

import aiohttp

# 테스트할 방법 설정
encoding_method = "hamming"  # 'pass', 'hamming', 'repetition'
modulation_method = "qpsk"  # 'qpsk', 'bpsk'
noise_method = "gaussian"  # 'gaussian', 'uniform'

# 원본 데이터 비트
original_bits = "11010011"


async def main():
    async with aiohttp.ClientSession() as session:
        # 1. 채널 코딩
        async with session.post(
            f"http://localhost:5001/encode/{encoding_method}",
            json={"data_bits": original_bits},
        ) as encode_resp:
            if encode_resp.status != 200:
                error = await encode_resp.json()
                print(f"Error {error['error_code']}: {error['error']}")
                return
            coded_bits_list = (await encode_resp.json())["coded_bits"]
            coded_bits = "".join(map(str, coded_bits_list))  # 리스트를 문자열로 변환

        # 2. 변조
        async with session.post(
            f"http://localhost:5002/modulate/{modulation_method}",
            json={"bits": coded_bits},
        ) as modulate_resp:
            if modulate_resp.status != 200:
                error = await modulate_resp.json()
                print(f"Error {error['error_code']}: {error['error']}")
                return
            symbols = (await modulate_resp.json())["symbols"]

        # 3. 노이즈 추가
        async with session.post(
            f"http://localhost:5003/add_noise/{noise_method}",
            json={"symbols": symbols, "snr_db": 10},
        ) as noise_resp:
            if noise_resp.status != 200:
                error = await noise_resp.json()
                print(f"Error {error['error_code']}: {error['error']}")
                return
            noisy_symbols = (await noise_resp.json())["noisy_symbols"]

        # 4. 복조
        async with session.post(
            f"http://localhost:5002/demodulate/{modulation_method}",
            json={"symbols": noisy_symbols},
        ) as demodulate_resp:
            if demodulate_resp.status != 200:
                error = await demodulate_resp.json()
                print(f"Error {error['error_code']}: {error['error']}")
                return
            demodulated_bits = (await demodulate_resp.json())["bits"]

        # 5. 채널 디코딩
        demodulated_bits_list = list(
            map(int, demodulated_bits)
        )  # 문자열을 리스트로 변환
        async with session.post(
            f"http://localhost:5001/decode/{encoding_method}",
            json={"coded_bits": demodulated_bits_list},
        ) as decode_resp:
            if decode_resp.status != 200:
                error = await decode_resp.json()
                print(f"Error {error['error_code']}: {error['error']}")
                return
            decoded_bits = (await decode_resp.json())["decoded_bits"]

        # 결과 출력
        print(f"Original Bits: {original_bits}")
        print(f"Decoded Bits:  {decoded_bits}")


# 비동기 함수 실행
asyncio.run(main())
