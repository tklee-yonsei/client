# 클라이언트

통신 API 서버를 위해 만들어진 클라이언트입니다.

본 프로젝트의 설명은 다음 링크에서 보실 수 있습니다.

https://hot-periwinkle-9ea.notion.site/d8c0797eff484f98b099cb9ed885965f

## 관련 작업

본 프로젝트의 github 및 연관 프로젝트의 github 주소는 다음과 같습니다.

- 팀1 - 채널 코딩/디코딩 - coder
    - https://github.com/tklee-yonsei/preprocess
- 팀2 - 변복조 - modulator
    - https://github.com/tklee-yonsei/modulator
- 팀3 - 노이즈 - noise
    - https://github.com/tklee-yonsei/noise
- 클라이언트
    - https://github.com/tklee-yonsei/client

## 시작하기

클라이언트를 다음 명령을 통해 실행할 수 있습니다.

Docker 이미지 빌드
```console
$ docker build -t async-client .
```

Docker 컨테이너 실행
```console
$ docker run --rm --network="host" -v $(pwd):/app async-client python async_client.py
```

## License

This project is licensed under the MIT License.
