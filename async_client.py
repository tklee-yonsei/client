import argparse
import asyncio
import aiohttp

def main():
    # 기본 서버 주소
    default_encode_server = "http://localhost:5001"
    default_modulate_server = "http://localhost:5002"
    default_noise_server = "http://localhost:5003"

    # 기본 설정 값
    default_encoding_method = "hamming"  # 'pass', 'hamming', 'repetition'
    default_modulation_method = "qpsk"  # 'qpsk', 'bpsk'
    default_noise_method = "gaussian"  # 'gaussian', 'uniform'
    default_original_bits = "11010011"

    # argparse를 사용하여 옵션 변수 처리
    parser = argparse.ArgumentParser(description="Async Client")
    parser.add_argument('--es', type=str, default=default_encode_server, help='Encoding server address')
    parser.add_argument('--ms', type=str, default=default_modulate_server, help='Modulate server address')
    parser.add_argument('--ns', type=str, default=default_noise_server, help='Noise server address')
    parser.add_argument('--em', type=str, default=default_encoding_method, help='Encoding method')
    parser.add_argument('--mm', type=str, default=default_modulation_method, help='Modulation method')
    parser.add_argument('--nm', type=str, default=default_noise_method, help='Noise method')
    parser.add_argument('--ob', type=str, default=default_original_bits, help='Original bits')
    args = parser.parse_args()

    encode_server = args.es
    modulate_server = args.ms
    noise_server = args.ns
    encoding_method = args.em
    modulation_method = args.mm
    noise_method = args.nm
    original_bits = args.ob

    print("사용할 서버 주소들:")
    print("Encoding Server:", encode_server)
    print("Modulate Server:", modulate_server)
    print("Noise Server:", noise_server)
    print("Encoding Method:", encoding_method)
    print("Modulation Method:", modulation_method)
    print("Noise Method:", noise_method)
    print("Original Bits:", original_bits)

    async def async_main():
        async with aiohttp.ClientSession() as session:
            print(f"original_bits: {original_bits}")

            # 1. 채널 코딩
            async with session.post(
                f"{encode_server}/encode/{encoding_method}",
                json={"data_bits": original_bits},
            ) as encode_resp:
                if encode_resp.status != 200:
                    error = await encode_resp.json()
                    print(f"Error {error['error_code']}: {error['error']}")
                    return
                coded_bits_list = (await encode_resp.json())["coded_bits"]
                coded_bits = "".join(map(str, coded_bits_list))  # 리스트를 문자열로 변환

            print(f"coded_bits: {coded_bits}")

            # 2. 변조
            async with session.post(
                f"{modulate_server}/modulate/{modulation_method}",
                json={"bits": coded_bits},
            ) as modulate_resp:
                if modulate_resp.status != 200:
                    error = await modulate_resp.json()
                    print(f"Error {error['error_code']}: {error['error']}")
                    return
                symbols = (await modulate_resp.json())["symbols"]

            print(f"symbols: {symbols}")

            # 3. 노이즈 추가
            async with session.post(
                f"{noise_server}/add_noise/{noise_method}",
                json={"symbols": symbols, "snr_db": 10},
            ) as noise_resp:
                if noise_resp.status != 200:
                    error = await noise_resp.json()
                    print(f"Error {error['error_code']}: {error['error']}")
                    return
                noisy_symbols = (await noise_resp.json())["noisy_symbols"]

            print(f"noisy_symbols: {noisy_symbols}")

            # 4. 복조
            async with session.post(
                f"{modulate_server}/demodulate/{modulation_method}",
                json={"symbols": noisy_symbols},
            ) as demodulate_resp:
                if demodulate_resp.status != 200:
                    error = await demodulate_resp.json()
                    print(f"Error {error['error_code']}: {error['error']}")
                    return
                demodulated_bits = (await demodulate_resp.json())["bits"]

            print(f"demodulated_bits: {demodulated_bits}")

            # 5. 채널 디코딩
            demodulated_bits_list = list(
                map(int, demodulated_bits)
            )  # 문자열을 리스트로 변환
            async with session.post(
                f"{encode_server}/decode/{encoding_method}",
                json={"coded_bits": demodulated_bits_list},
            ) as decode_resp:
                if decode_resp.status != 200:
                    error = await decode_resp.json()
                    print(f"Error {error['error_code']}: {error['error']}")
                    return
                decoded_bits = (await decode_resp.json())["decoded_bits"]

            print(f"decoded_bits: {decoded_bits}")

            # 결과 출력
            print(f"Original Bits: {original_bits}")
            print(f"Decoded Bits:  {decoded_bits}")

    # 비동기 함수 실행
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
