# seoul-subway

Seoul Subway information skill for Claude.

서울 지하철 정보 스킬입니다.

## Features / 기능

- **Real-time Arrival / 실시간 도착정보** - Train arrival times by station
- **Station Search / 역 검색** - Line and station code lookup
- **Route Search / 경로 검색** - Shortest path, travel time, fare
- **Service Alerts / 운행 알림** - Delays, incidents, express stops

## Usage / 사용법

```
"강남역 도착정보" / "Gangnam station arrivals"
"강남역 몇호선?" / "What line is Gangnam?"
"신도림에서 서울역" / "Sindorim to Seoul Station"
"지하철 지연 있어?" / "Any subway delays?"
```

---

## API Keys / API 인증키 발급

This skill requires two API keys. Follow the steps below carefully.

이 스킬은 두 개의 API 키가 필요합니다. 아래 단계를 따라주세요.

### 1. SEOUL_OPENAPI_KEY

> Provider: Seoul Open Data Plaza (서울 열린데이터 광장)

**Direct Link / 바로가기**: [인증키 신청](https://data.seoul.go.kr/together/mypage/actkeyMain.do)

#### English

1. Go to [API Key Request Page](https://data.seoul.go.kr/together/mypage/actkeyMain.do)
2. Login or Sign Up (foreign users can sign up with email)
3. Find **실시간 지하철 인증키 신청** (Real-time Subway API Key Request) and click it
4. Fill in the form (just write anything):
   - 용도 (Purpose): `개인` or `Personal use`
   - 환경 (Environment): `기타` or `Other`
   - 내용 (Description): `subway app` or anything
5. Copy your API key
6. **Wait 5-30 minutes** for the key to activate before using

#### 한국어

1. [인증키 신청 페이지](https://data.seoul.go.kr/together/mypage/actkeyMain.do) 접속
2. 로그인 또는 회원가입
3. **실시간 지하철 인증키 신청** 클릭
4. 신청서 작성 (대충 적으면 됨):
   - 용도: `개인`
   - 환경: `기타`
   - 내용: `지하철 앱` 등 아무거나
5. 인증키 복사
6. **5~30분 대기** 후 사용 가능 (바로 사용 시 오류 발생)

---

### 2. DATA_GO_KR_KEY

> Provider: Public Data Portal (공공데이터포털)

**Direct Links / 바로가기**:
| API | English | 한국어 |
|-----|---------|--------|
| 서울교통공사_지하철알림정보 | [Link](https://www.data.go.kr/en/data/15144070/openapi.do) | [링크](https://www.data.go.kr/data/15144070/openapi.do) |
| 서울교통공사_최단경로이동정보 | [Link](https://www.data.go.kr/en/data/15143842/openapi.do) | [링크](https://www.data.go.kr/data/15143842/openapi.do) |

#### English

1. Go to each API link above
2. Login or Sign Up (foreign users can use email verification)
3. Click **활용신청** (Request Access)
4. Fill in the form:
   - 활용목적: `앱 개발` (App Development)
   - Check the agreement boxes
5. Approval is usually **instant**
6. Go to **마이페이지** → **오픈API** → **인증키 발급현황**
7. Copy your **일반 인증키 (Encoding)** - this is your API key

#### 한국어

1. 위 API 링크 각각 접속
2. 로그인 또는 회원가입
3. **활용신청** 버튼 클릭
4. 신청서 작성:
   - 활용목적: `앱 개발` 선택
   - 동의 체크박스 선택
5. 보통 **즉시 승인**됩니다
6. **마이페이지** → **오픈API** → **인증키 발급현황** 이동
7. **일반 인증키 (Encoding)** 복사 - 이게 API 키입니다

> **Note**: API keys may take **5-30 minutes** to activate after issuance. If you get errors, please wait and try again.
>
> **참고**: API 키 발급 후 **5~30분** 정도 지나야 활성화될 수 있습니다. 오류가 발생하면 잠시 후 다시 시도해주세요.

---

## Environment Variables Setup / 환경변수 설정

#### macOS / Linux

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export SEOUL_OPENAPI_KEY="your-seoul-api-key-here"
export DATA_GO_KR_KEY="your-data-go-kr-key-here"
```

Then reload:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

#### Windows (PowerShell)

```powershell
[System.Environment]::SetEnvironmentVariable("SEOUL_OPENAPI_KEY", "your-seoul-api-key-here", "User")
[System.Environment]::SetEnvironmentVariable("DATA_GO_KR_KEY", "your-data-go-kr-key-here", "User")
```

Restart your terminal after setting.

설정 후 터미널을 재시작하세요.

---

## Troubleshooting / 문제 해결

### "API key is not configured" error

- Check if environment variables are set correctly: `echo $SEOUL_OPENAPI_KEY`
- Restart your terminal or Claude Desktop after setting

### "Invalid API key" error

- Make sure you copied the **Encoding** key, not the Decoding key
- Check for extra spaces or newlines in your key

### API request fails

- data.go.kr APIs may take a few minutes to activate after approval
- Try again after 5-10 minutes

---

## License

MIT
