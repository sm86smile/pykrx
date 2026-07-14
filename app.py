
어제 오후 11:26

README (1).md
파일
해당 readme 파일 참고해서 streamlit에서 앱으로 실행을 하고 싶은데 어떻게 해야하는지 중학생도 알아들을 수 있게 순서대로 설명해줘

32s 동안 처리함
<output>
오류 원인은 두 가지가 겹쳤을 가능성이 큽니다.

저장소를 GitHub에서 ZIP으로 다운로드해 .git 정보가 없습니다.

폴더 경로에 작은따옴표와 공백이 있습니다.

C:\Users\Man's\Downloads\99_Chrome download\pykrx-master
오류에 표시된 %27은 작은따옴표 ', %20은 공백을 뜻합니다.

더 중요한 원인은 첫 번째입니다. 이 저장소의 pyproject.toml은 버전 번호를 setuptools_scm으로 자동 생성하도록 설정돼 있습니다. GitHub ZIP에는 보통 .git 이력이 포함되지 않기 때문에 버전을 계산하지 못해 editable 설치가 실패할 수 있습니다. 저장소는 setuptools_scm과 동적 버전을 사용하도록 구성돼 있습니다. 

가장 쉬운 해결 방법
PyKRX 소스 자체를 수정하려는 것이 아니라 Streamlit 앱에서 PyKRX를 사용하려는 목적이라면 pip install -e .를 실행할 필요가 없습니다.

현재 PowerShell에서 다음 명령을 실행하세요.

python -m pip install --upgrade pip
python -m pip install pykrx streamlit pandas
설치 확인:

python -c "from pykrx import stock; print('PyKRX 설치 성공')"
다음 결과가 나오면 정상입니다.

PyKRX 설치 성공
그다음 app.py가 있는 폴더에서 실행합니다.

python -m streamlit run app.py
PyKRX 공식 README에서도 일반 사용자는 다음 명령으로 설치하도록 안내합니다. 

pip install pykrx
현재 만들어진 잘못된 설치 흔적 정리
현재 가상환경을 그대로 사용해도 되지만, 깨끗하게 다시 만드는 방법이 가장 안전합니다.

먼저 PowerShell을 닫습니다.

그다음 다음처럼 작은따옴표와 공백이 없는 폴더를 만드세요.

C:\pykrx_app
현재 필요한 app.py 파일만 이 폴더로 옮깁니다.

최종 구조:

C:\pykrx_app
├── app.py
└── requirements.txt
PowerShell을 열고 다음 명령을 한 줄씩 실행합니다.

cd C:\pykrx_app
py -3.11 -m venv .venv
Python 3.11이 없다고 나오면:

py -m venv .venv
가상환경 실행:

.\.venv\Scripts\Activate.ps1
권한 오류가 나면:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
그다음 다시:

.\.venv\Scripts\Activate.ps1
설치:

python -m pip install --upgrade pip setuptools wheel
python -m pip install pykrx streamlit pandas
실행:

python -m streamlit run app.py
requirements.txt 내용도 수정
앞서 작성한 requirements.txt에 다음과 같이 적혀 있다면:

streamlit
-e .
-e .를 삭제하세요.

다음처럼 작성하면 됩니다.

streamlit
pykrx
pandas
-e .는 현재 폴더의 프로젝트를 editable 방식으로 설치한다는 뜻입니다. pip는 로컬 프로젝트를 pip install . 또는 editable 방식인 pip install -e .로 설치할 수 있지만, 해당 저장소의 빌드 설정이 정상적으로 처리돼야 합니다. 

PyKRX 소스 코드를 직접 수정할 때만 사용하는 방법
본인의 sm86smile/pykrx 저장소 안에 있는 PyKRX 라이브러리 코드를 직접 수정하고 시험하려는 경우에는 ZIP 대신 git clone을 사용해야 합니다.

1. Git 설치 확인
git --version
버전이 나오면 정상입니다.

2. 안전한 경로로 이동
cd C:\
3. 저장소 복제
git clone https://github.com/sm86smile/pykrx.git pykrx-source
4. 폴더 이동
cd C:\pykrx-source
5. 가상환경 생성
py -3.11 -m venv .venv
6. 가상환경 실행
.\.venv\Scripts\Activate.ps1
7. 빌드 도구 업데이트
python -m pip install --upgrade pip setuptools wheel setuptools-scm
8. editable 설치
python -m pip install -e .
개발 도구까지 설치하려면:

python -m pip install -e ".[dev]"
git clone으로 받으면 .git 정보가 함께 내려오기 때문에 setuptools_scm이 프로젝트 버전을 계산할 수 있습니다.

지금 사용자에게 권장하는 방법
Streamlit 앱을 실행하는 것이 목적이므로 GitHub의 PyKRX 전체 소스를 설치하지 말고 다음 방식으로 진행하세요.

mkdir C:\pykrx_app
cd C:\pykrx_app
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit pykrx pandas
python -m streamlit run app.py
그리고 requirements.txt는 다음으로 변경합니다.

streamlit
pykrx
pandas
즉, 이번 오류가 발생한 명령:

python -m pip install -e .
은 건너뛰어도 됩니다.

</output> <reflection>
현재 제공된 문장은 설치 오류의 마지막 한 줄이라 세부 원인을 100% 확정할 수는 없습니다. 다만 pykrx-master라는 ZIP 압축 해제 폴더명과 setuptools_scm 빌드 설정을 볼 때, Git 메타데이터 없이 editable 설치를 시도한 것이 가장 유력합니다. 경로의 작은따옴표와 공백도 문제 가능성을 줄이기 위해 피하는 것이 안전합니다.

</reflection>

14번 실행 시 아래 에러 확인해줘
note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'file:///C:/Users/Man%27s/Downloads/99_Chrome%20download/pykrx-master' when getting requirements to build editable

45s 동안 처리함
<thinking> 오류 경로를 보면 `requirements.txt`가 현재 폴더를 editable 방식으로 다시 설치하려고 시도하고 있습니다. </thinking> <output>
원인
14번에서 실행한 명령이 다음이었다면,

python -m pip install -r requirements.txt
requirements.txt 안에 아직 아래 줄이 들어 있는 것입니다.

-e .
-e .는 다음 뜻입니다.

현재 폴더의 프로젝트를 editable 방식으로 설치
그래서 pip가 다시 아래 폴더를 빌드하려고 한 것입니다.

C:\Users\Man's\Downloads\99_Chrome download\pykrx-master
현재 저장소는 버전을 고정된 숫자로 적지 않고 setuptools_scm이 Git 태그에서 자동 계산하도록 설정돼 있습니다. 그런데 ZIP으로 내려받은 폴더에는 .git 정보가 없어서 editable 빌드 과정이 실패할 수 있습니다. pyproject.toml에도 setuptools_scm과 동적 버전 설정이 확인됩니다. 

1. requirements.txt 내용 확인
현재 폴더에서 다음 명령을 실행하세요.

Get-Content .\requirements.txt
다음처럼 나온다면 잘못된 상태입니다.

streamlit
-e .
또는 다음 중 하나가 들어 있어도 삭제해야 합니다.

.
-e .
file:///C:/Users/...
2. requirements.txt를 완전히 덮어쓰기
PowerShell에서 다음 명령을 그대로 실행하세요.

@(
    "streamlit"
    "pykrx"
    "pandas"
) | Set-Content -Encoding ascii .\requirements.txt
다시 확인합니다.

Get-Content .\requirements.txt
반드시 아래 세 줄만 나와야 합니다.

streamlit
pykrx
pandas
3. 다시 설치
먼저 설치 도구를 업데이트합니다.

python -m pip install --upgrade pip setuptools wheel
그다음 캐시를 사용하지 않고 설치합니다.

python -m pip install --no-cache-dir -r requirements.txt
이제 오류 메시지에 다음 경로가 나오면 안 됩니다.

file:///C:/Users/Man%27s/Downloads/...
4. 설치 확인
python -c "import streamlit; import pandas; from pykrx import stock; print('설치 성공')"
정상 결과:

설치 성공
5. Streamlit 실행
현재 폴더에 app.py가 있는지 먼저 확인합니다.

dir app.py
파일이 확인되면 실행합니다.

python -m streamlit run app.py
브라우저가 자동으로 열리지 않으면 다음 주소로 접속합니다.

http://localhost:8501
그래도 동일한 오류가 나오면
현재 명령을 실행하는 폴더의 requirements.txt가 아닌 다른 파일을 수정했을 수 있습니다. 다음 두 명령으로 정확한 현재 위치와 파일 내용을 확인하세요.

Get-Location
Get-Content .\requirements.txt
출력은 대략 다음과 같아야 합니다.

Path
----
C:\Users\Man's\Downloads\99_Chrome download\pykrx-master
streamlit
pykrx
pandas
Get-Content 결과에 -e .가 한 줄이라도 남아 있으면 같은 오류가 반복됩니다.

더 안전한 권장 방법
현재 폴더는 PyKRX 라이브러리 소스와 Streamlit 앱이 섞여 있습니다. 앱만 실행하려면 별도 폴더로 분리하는 것이 가장 안전합니다.

mkdir C:\pykrx_app
Copy-Item .\app.py C:\pykrx_app\app.py
cd C:\pykrx_app
새 requirements.txt를 만듭니다.

@(
    "streamlit"
    "pykrx"
    "pandas"
) | Set-Content -Encoding ascii .\requirements.txt
새 가상환경을 만듭니다.

py -3.11 -m venv .venv
Python 3.11이 없으면:

py -m venv .venv
가상환경 실행:

.\.venv\Scripts\Activate.ps1
설치 및 실행:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
이번 오류를 바로 해결하는 핵심은 다음 한 줄입니다.

requirements.txt에서 -e . 삭제
</output> <reflection> 이번 오류는 pip 자체의 문제라기보다 `requirements.txt`가 현재 ZIP 저장소를 editable 프로젝트로 다시 빌드하도록 지시해서 발생한 것입니다. `pykrx`를 일반 패키지로 설치하면 로컬 editable 빌드가 필요하지 않습니다. </reflection>

sm86smile/pykrx폴더 내 readme안에 있는 기능처럼 폴더 내 모든 파일을 확인해서 모든 기능을 streamlit에서 사용하도록 app.py 코드 수정해줘

7m 12s 동안 처리함
저장소의 공개 API 구조를 기준으로 **주식·수급·지수·공매도·ETF/ETN/ELW·선물·채권 기능을 Streamlit에서 실행할 수 있는 통합 app.py**를 작성했습니다.

현재 저장소에서 stock 모듈은 stock_api.py와 future_api.py의 공개 기능을 내보내고, bond 모듈은 bond.py의 공개 기능을 내보내는 구조입니다. README에 설명된 시장 데이터, 지수, 공매도, ETF, 채권 기능도 이 모듈들을 통해 제공됩니다. 

다운로드
app.py

requirements.txt

Secrets 예제 다운로드

전체 파일 ZIP 다운로드

포함된 화면
1. 쉬운 조회
자주 사용하는 기능을 항목별로 선택할 수 있습니다.

주식 OHLCV·시가총액·PER/PBR·가격 변동

외국인 보유량·한도소진율

투자자별 거래대금·거래량·순매수 상위종목

지수 목록·구성종목·OHLCV·기본지표

공매도 거래·잔고·TOP 50

ETF·ETN·ELW 목록·가격·구성종목

ETF 괴리율·추적오차·투자자 거래

선물 상품·OHLCV

채권 수익률

영업일·종목명·기업 주요 변동사항

2. 전체 API 실행기
stock과 bond 모듈에서 이름이 get_으로 시작하는 공개 함수를 자동으로 찾아 화면에 표시합니다.

따라서 현재 API뿐 아니라 나중에 저장소에 공개 함수가 추가돼도 자동으로 목록에 나타납니다.

다만 pykrx/website 내부의 KRX·네이버 통신용 함수는 라이브러리 내부 구현이므로 직접 실행 대상으로 넣지 않았습니다. 사용자용 공개 API인 stock과 bond 기능을 대상으로 구성했습니다. 저장소의 stock 패키지는 future_api.py와 stock_api.py를 공개하고, bond 패키지는 bond.py를 공개합니다. 

3. API 목록
다음 내용을 표로 확인하고 CSV로 내려받을 수 있습니다.

모듈

기능 분류

함수 이름

함수 호출 형식

함수 설명

4. 결과 기능
모든 조회 결과에 다음 기능을 적용했습니다.

표 출력

행·열 개수 표시

숫자 데이터 차트

CSV 또는 JSON 다운로드

호출한 함수와 인자 표시

오류 상세내용 표시

마지막 결과 유지·삭제

파일 넣는 위치
다운로드한 app.py와 requirements.txt를 저장소의 가장 바깥쪽에 넣습니다.

pykrx-master
├── app.py
├── requirements.txt
├── README.md
├── pyproject.toml
├── pykrx
│   ├── stock
│   ├── bond
│   └── website
└── tests
기존 requirements.txt에 다음 내용이 있다면 완전히 교체하세요.

-e .
새로 전달한 requirements.txt에는 -e .가 없습니다.

또한 pykrx도 별도로 설치하지 않습니다. 앱이 저장소 안의 다음 로컬 소스를 직접 사용하기 때문입니다.

pykrx-master\pykrx
새 requirements.txt 내용은 다음과 같습니다.

streamlit>=1.36
requests>=2.32.0
pandas>=2.2.0,<3.0
numpy>=2.0
deprecated>=1.2.14
multipledispatch>=1.0.0
matplotlib>=3.8.0
기존 가상환경 삭제
앞서 editable 설치 오류가 발생했던 가상환경을 지우고 새로 만드는 것이 안전합니다.

PowerShell에서 저장소 폴더로 이동합니다.

cd "C:\Users\Man's\Downloads\99_Chrome download\pykrx-master"
기존 가상환경이 활성화돼 있다면 종료합니다.

deactivate
기존 .venv를 삭제합니다.

Remove-Item -Recurse -Force .venv
삭제할 폴더가 없다는 메시지가 나오면 그대로 넘어가면 됩니다.

새 가상환경 만들기
Python 3.11을 사용하는 경우:

py -3.11 -m venv .venv
Python 3.11을 찾지 못한다면:

py -m venv .venv
가상환경을 실행합니다.

.\.venv\Scripts\Activate.ps1
스크립트 실행 제한 오류가 나오면:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
그리고 다시 실행합니다.

.\.venv\Scripts\Activate.ps1
정상적으로 실행되면 PowerShell 왼쪽에 표시됩니다.

(.venv)
라이브러리 설치
다음 명령을 순서대로 실행합니다.

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
이번에는 아래 설치 명령을 실행하지 않습니다.

python -m pip install -e .
다음 명령도 별도로 실행하지 않습니다.

python -m pip install pykrx
앱이 저장소에 들어 있는 로컬 pykrx 코드를 직접 불러옵니다.

앱 실행
저장소 루트에서 실행합니다.

python -m streamlit run app.py
정상적으로 실행되면 다음과 비슷하게 표시됩니다.

Local URL: http://localhost:8501
브라우저가 자동으로 열리지 않으면 다음 주소로 접속합니다.

http://localhost:8501
제가 작성한 파일은 Python 구문 검사를 통과했고, Streamlit 서버가 실제로 시작되는 것까지 확인했습니다.

KRX 로그인 설정
저장소 README에서는 일부 인증 필요 API를 위해 KRX_ID와 KRX_PW 환경변수를 요구합니다. 환경변수가 없으면 인증이 필요한 데이터 조회가 실패할 수 있습니다. 

저장소 루트에 다음 폴더를 만듭니다.

.streamlit
그 안에 다음 파일을 만듭니다.

secrets.toml
최종 위치:

pykrx-master
├── .streamlit
│   └── secrets.toml
├── app.py
├── requirements.txt
└── pykrx
secrets.toml 내용:

KRX_ID = "본인의_KRX_아이디"
KRX_PW = "본인의_KRX_비밀번호"
전달한 secrets.toml.example 파일을 다음 위치로 복사해도 됩니다.

New-Item -ItemType Directory -Force .streamlit
Copy-Item secrets.toml.example .streamlit\secrets.toml
그다음 .streamlit\secrets.toml을 열어 실제 아이디와 비밀번호를 입력합니다.

secrets.toml은 GitHub에 올리면 안 됩니다. .gitignore에 다음 줄을 추가하세요.

.streamlit/secrets.toml
가장 간단한 실행 명령 정리
cd "C:\Users\Man's\Downloads\99_Chrome download\pykrx-master"

py -3.11 -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

python -m pip install -r requirements.txt

python -m streamlit run app.py
이번 버전에서는 문제가 됐던 다음 과정이 완전히 제거됐습니다.

requirements.txt의 -e .
→ 현재 저장소 editable 빌드 시도
→ Failed to build file:///.../pykrx-master
따라서 이전에 발생했던 editable 빌드 오류를 거치지 않고 앱을 실행할 수 있습니다.


readme 파일 안에 목차에 나오는 모든 기능을 사용할 수 있도록 수정해줘

11m 1s 동안 처리함
README 목차에 나온 기능을 기준으로 app.py를 전면 수정했습니다. README는 주식 시세·수급·지수·공매도·ETF/ETN/ELW·채권·기업 변동사항 API를 설명하고 있습니다. 

수정 파일
app.py

전체 실행 파일 ZIP 다운로드

requirements.txt

Secrets 예제 다운로드

이번에 추가·보완된 내용
README 목차 43개 기능을 화면에 구성
README 전체 기능 탭에서 다음 순서대로 선택할 수 있습니다.

MarketData API 15개

인덱스 API 6개

공매도 API 8개

ETF API 8개

ETN API

ELW API

채권 API 3개

기업정보 API

README에 등장하는 함수 46개 확인
README 기능 확인 탭에서 다음 내용을 확인할 수 있습니다.

README 함수명

현재 설치된 PyKRX에서 사용 가능한지

실제 연결된 함수명

버전 차이로 대체된 호환 함수

함수 호출 형식

예를 들어 아래처럼 이름이 달라진 경우에도 자동으로 호환합니다.

get_market_ohlcv
→ get_market_ohlcv_by_date
→ get_market_ohlcv_by_ticker
get_shorting_trade_top50
→ get_shorting_volume_top50
get_etf_trading_volumne_and_value
→ get_etf_trading_volume_and_value
ETF 거래실적 네 가지 방식 추가
기존 코드에서 부족했던 README의 ETF 거래실적 호출 방식을 모두 넣었습니다.

기간 전체 ETF 투자자별 집계

기간 개별 상품 투자자별 집계

일자별 전체 ETF 거래대금·거래량

일자별 개별 상품 거래대금·거래량

각 방식에서 다음을 선택할 수 있습니다.

거래대금 / 거래량
순매수 / 매수 / 매도
모든 공개 API 자동 실행기 유지
README에 아직 설명되지 않은 함수나 나중에 추가되는 함수도 사용할 수 있도록 다음 모듈의 모든 get_* 함수를 자동으로 읽습니다.

from pykrx import stock
from pykrx import bond
전체 공개 API 실행기 탭에서 함수 이름, 설명, 호출 인자를 확인하고 실행할 수 있습니다.

README의 지표 수익률 처리
README에는 지표 수익률이라는 목차가 있지만 함수명과 실행 예제가 비어 있습니다. 따라서 임의의 함수를 연결하지 않고, 앱 화면에서 문서에 실행 함수가 정의되지 않았다고 안내하도록 했습니다. 현재 설치된 PyKRX에 관련 함수가 추가된 경우에는 전체 공개 API 실행기의 bond 모듈에 자동으로 나타납니다. 

파일 교체 방법
기존 저장소의 가장 바깥쪽에 있는 app.py를 새 파일로 교체합니다.

pykrx-master
├── app.py                 ← 새 파일로 교체
├── requirements.txt
├── README.md
├── pyproject.toml
├── pykrx
│   ├── stock
│   ├── bond
│   └── website
└── tests
PowerShell에서 저장소 폴더로 이동합니다.

cd "C:\Users\Man's\Downloads\99_Chrome download\pykrx-master"
가상환경을 실행합니다.

.\.venv\Scripts\Activate.ps1
실행 정책 오류가 나오면 먼저 다음을 실행합니다.

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
다시 가상환경을 실행합니다.

.\.venv\Scripts\Activate.ps1
필요한 패키지를 설치합니다.

python -m pip install -r requirements.txt
앱을 실행합니다.

python -m streamlit run app.py
브라우저가 자동으로 열리지 않으면 다음 주소로 접속합니다.

http://localhost:8501
검사 결과
다음 검사를 완료했습니다.

Python 구문 검사 통과

Streamlit 서버 기동 확인

README 메뉴 43개 화면 생성 검사 통과

43개 메뉴에서 화면 중복 위젯 오류 없음

실제 조회 버튼이 있는 42개 메뉴의 기본 호출 검사 통과

결과가 두 탭에 표시될 때 발생할 수 있는 Streamlit 위젯 키 중복 문제 수정

최신 Streamlit의 width="stretch" 방식으로 변경

실제 KRX 서버 응답은 계정 인증, 조회일, 데이터 제공 시점과 네트워크 상태에 따라 달라지므로 모든 실데이터 호출까지 검증한 것은 아닙니다. 실행 중 특정 기능에서 오류가 나오면 오류 메시지 전체를 보내주면 해당 함수의 실제 인자 형식에 맞춰 조정할 수 있습니다.


에러 확인해줘

로그인이 필요한 API라면 .streamlit/secrets.toml에 KRX_ID와 KRX_PW를 설정하고, 조회일이 휴일인지 또는 데이터 제공 시점이 지났는지 확인하세요.

31s 동안 처리함

Traceback (most recent call last):
  File "/mount/src/pykrx/app.py", line 198, in run_call
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/mount/src/pykrx/pykrx/stock/stock_api.py", line 2169, in get_shorting_balance
    return get_shorting_balance_by_ticker(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mount/src/pykrx/pykrx/stock/stock_api.py", line 35, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
TypeError: get_shorting_balance_by_ticker() missing 1 required positional argument: 'date'

4m 39s 동안 처리함
원인은 KRX 로그인 문제가 아니라 필수 날짜 인자가 빠진 것입니다.

오류가 난 호출 흐름은 다음과 같습니다.

get_shorting_balance()
→ get_shorting_balance_by_ticker()
→ date 인자가 없음
→ TypeError
get_shorting_balance는 실제로 두 가지 방식으로 호출해야 합니다.

# 특정 종목의 기간별 공매도 잔고
stock.get_shorting_balance(
    "20260701",
    "20260710",
    "005930",
)
# 특정일 시장 전체 공매도 잔고
stock.get_shorting_balance(
    "20260710",
    market="KOSPI",
)
내부의 get_shorting_balance_by_ticker는 date가 필수이고, get_shorting_balance_by_date는 시작일·종료일·종목코드가 필수입니다. 

왜 앱에서 날짜가 빠졌나
전체 공개 API 실행기가 해당 함수의 형식을 다음처럼 인식했습니다.

get_shorting_balance(*args, **kwargs)
이처럼 여러 호출 방식을 지원하는 함수는 Python이 구체적인 필수 인자를 자동으로 알아내지 못합니다. 기존 앱에서는 위치 인자가 빈 배열로 남아 다음처럼 실행됐습니다.

get_shorting_balance(*[], **{})
그래서 date가 없다는 오류가 발생했습니다.

수정한 내용
수정된 앱에서는 get_shorting_balance를 선택하면 다음 두 가지 조회 방식이 나타납니다.

기간별 개별 종목
입력 항목:

시작일
종료일
종목코드
실제 호출:

get_shorting_balance(
    시작일,
    종료일,
    종목코드,
)
특정일 전종목
입력 항목:

조회일
시장: KOSPI / KOSDAQ / KONEX
실제 호출:

get_shorting_balance(
    조회일,
    market=시장,
)
또한 같은 문제가 반복될 수 있는 다음 동적 인자 함수에도 전용 입력 화면을 추가했습니다.

get_market_ohlcv
get_market_cap
get_market_fundamental
get_exhaustion_rates_of_foreign_investment
get_market_price_change
get_index_ohlcv
get_index_fundamental
get_shorting_balance
get_etf_trading_volume_and_value
get_future_ohlcv
get_previous_business_days
get_otc_treasury_yields
필수 인자가 빠진 TypeError가 발생하면 더 이상 로그인 안내를 우선 표시하지 않고, 날짜·종목코드 등의 필수 입력값 누락 오류라고 구분해 표시하도록 수정했습니다.

수정된 파일
app.py

수정 파일 전체 ZIP 다운로드

GitHub에 적용하는 방법
GitHub 저장소의 기존 app.py를 다운로드한 새 app.py로 교체합니다.

pykrx
├── app.py   ← 수정된 파일로 교체
├── requirements.txt
├── pyproject.toml
└── pykrx
GitHub 웹 화면에서는 기존 app.py를 열고 다음 순서로 진행합니다.

연필 아이콘 Edit
→ 기존 코드 전체 삭제
→ 수정된 app.py 내용 붙여넣기
→ Commit changes
Streamlit Cloud가 자동으로 다시 배포하지 않으면 앱 관리 화면에서 재부팅합니다.

수정 후 확인 방법
앱에서 다음 순서로 선택합니다.

전체 공개 API 실행기
→ stock
→ get_shorting_balance
그다음 조회 방식을 선택합니다.

기간별 개별 종목
예시:

시작일: 2026-07-01
종료일: 2026-07-10
종목코드: 005930
또는:

특정일 전종목
조회일: 2026-07-10
시장: KOSPI
화면 아래에 다음과 같은 실행 예정 인자가 표시되면 정상입니다.

args=['20260710']
kwargs={'market': 'KOSPI'}
수정된 파일은 Python 구문 검사와 Streamlit 화면 생성 검사를 통과했고, get_shorting_balance의 두 조회 방식 모두 날짜 인자가 정상적으로 생성되는 것을 확인했습니다.


종목코드 대신에 종목이름으로 조회 할 수 있게 해주고 종목이름은 잘 모를경우를 대비해서 일부만 작성해도 자동완성해서 리스트를 보여준 다음 선택하는 기능도 넣어주면 좋겠어 그리고 종목별 말고 전체 종목에 대해서도 한번에 조회할 수 있게 해줘

16m 21s 동안 처리함
요청한 기능을 반영해 app.py를 수정했습니다.

수정 파일
app.py

전체 파일 ZIP 다운로드

requirements.txt

Secrets 설정 예제

1. 종목명 검색 및 자동완성
기존 종목코드 직접 입력 방식을 다음 구조로 변경했습니다.

종목명의 일부 또는 종목코드 일부 입력

일치하는 종목 목록 자동 표시

목록에서 원하는 종목 선택

선택한 종목의 이름·코드·시장 확인

예를 들어 검색창에 다음처럼 입력할 수 있습니다.

삼성
하이닉스
에이
0059
검색 결과는 다음처럼 표시됩니다.

삼성전자 (005930) · KOSPI
삼성전자우 (005935) · KOSPI
검색할 때는 공백과 영문 대소문자를 구분하지 않습니다.

sk하이닉스
SK 하이닉스
sk 하이닉스
모두 SK하이닉스를 찾을 수 있습니다.

종목명 목록을 불러오지 못하면 앱이 멈추지 않고 자동으로 종목코드 직접 입력 방식으로 전환됩니다.

2. 적용된 자동완성 대상
다음 상품에 이름 검색과 자동완성을 적용했습니다.

코스피 주식

코스닥 주식

코넥스 주식

ETF

ETN

ELW

코스피 지수

코스닥 지수

전체 공개 API 실행기에서 함수의 입력 인자가 ticker인 경우에도 가능한 한 이름 검색 방식으로 표시됩니다.

3. 전체 종목 조회 기능
개별 종목을 조회하던 화면에는 다음 선택 항목이 나타납니다.

조회 범위

○ 개별 종목
○ 전체 종목
전체 종목을 선택하면 시장을 선택할 수 있습니다.

KOSPI
KOSDAQ
KONEX
ALL
공매도처럼 API에서 ALL 시장을 지원하지 않는 기능은 다음 시장만 표시됩니다.

KOSPI
KOSDAQ
KONEX
4. 특정일 전체 종목 조회
한 번의 API 호출로 전체 종목을 조회할 수 있는 기능은 다음처럼 표시됩니다.

특정일 전체 종목(빠름)
다음 기능에 적용했습니다.

특정일 전체 종목 OHLCV

특정일 전체 종목 PER·PBR·BPS·EPS

특정일 전체 종목 시가총액

특정일 전체 종목 외국인 보유량

특정일 전체 종목 공매도 거래량

특정일 전체 종목 공매도 잔고

이 방식은 종목마다 별도로 호출하지 않고 KRX의 전종목 API를 한 번 호출하므로 상대적으로 빠릅니다.

5. 기간별 전체 종목 조회
기간별 데이터는 대부분 종목코드를 하나씩 넣어야 하므로 다음 방식을 추가했습니다.

기간별 전체 종목(반복 호출)
다음 기능에서 사용할 수 있습니다.

기간별 OHLCV

기간별 PER·PBR·BPS·EPS

기간별 시가총액

기간별 외국인 보유량

기간별 공매도 현황

기간별 공매도 거래량

기간별 공매도 잔고

전체 종목 기업 주요 변동사항

실행 중에는 다음처럼 진행 상태가 표시됩니다.

15/943 · 삼성전자 (005930) 조회 중
모든 결과는 다음 열이 추가된 하나의 표로 합쳐집니다.

종목코드
종목명
시장
날짜
조회 데이터
CSV 파일로도 내려받을 수 있습니다.

6. 전체 종목 조회 안전장치
기간별 전체 종목 조회는 수백에서 수천 번 API를 호출할 수 있으므로 안전장치를 추가했습니다.

일부 종목만 시험
☑ 테스트용으로 일부 종목만 조회
이를 선택하면 최대 조회 종목 수를 지정할 수 있습니다.

조회할 최대 종목 수: 20
전체 조회 전에 먼저 10~20개 종목으로 시험하는 것을 권장합니다.

종목 간 호출 간격
기본값은 다음과 같습니다.

1.0초
README에서 반복 호출 시 1초 정도 간격을 두도록 안내한 내용을 반영했습니다.

전체 조회 확인
다음 확인란을 선택해야 실행 버튼이 활성화됩니다.

943개 종목 반복 조회와 호출 제한 위험을 확인했습니다.
연속 오류 자동 중단
로그인 실패, 요청 제한 또는 서버 차단 등으로 20개 종목이 연속해서 실패하면 불필요한 추가 호출을 막기 위해 자동으로 중단합니다.

실패한 종목은 별도 표와 CSV로 확인할 수 있습니다.

7. 전체 종목 수급 조회
다음 기능은 종목마다 반복 호출하지 않고 조회 대상에서 시장 전체를 선택할 수 있습니다.

일자별 투자자 거래대금

일자별 투자자 거래량

투자자별 거래대금

투자자별 거래량

예를 들어 조회 범위를 전체 종목으로 선택하고 시장을 KOSPI로 지정하면 함수에는 종목코드 대신 다음 값이 전달됩니다.

"KOSPI"
전체 시장을 합쳐서 조회할 수 있는 기능은 다음도 사용할 수 있습니다.

"ALL"
8. 전체 종목 결과에 종목명 추가
PyKRX의 전종목 조회 결과는 인덱스가 종목코드만 나오는 경우가 많습니다.

기존:

티커
005930
000660
278470
수정 후:

티커      종목명       시장
005930    삼성전자     KOSPI
000660    SK하이닉스   KOSPI
278470    에이피알     KOSDAQ
ETF·ETN·ELW·지수 목록도 가능한 경우 이름을 함께 표시합니다.

9. 종목 목록 캐시
종목명 자동완성을 사용할 때마다 KRX에서 목록을 다시 조회하지 않도록 종목 목록을 하루 동안 저장합니다.

사이드바에는 다음 버튼을 추가했습니다.

종목 목록 새로고침
신규 상장이나 종목명 변경이 반영되지 않을 때 이 버튼을 누르면 최신 목록을 다시 불러옵니다.

GitHub 적용 방법
GitHub 저장소에서 기존 app.py를 새 파일로 교체합니다.

저장소 구조는 다음과 같아야 합니다.

pykrx
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── pykrx
    ├── stock
    ├── bond
    └── website
GitHub 웹에서 적용한다면 다음 순서로 진행합니다.

app.py 열기
→ 연필 모양 Edit 버튼
→ 기존 코드 전체 삭제
→ 새 app.py 코드 붙여넣기
→ Commit changes
Streamlit Community Cloud가 자동으로 재실행하지 않으면 앱 관리 화면에서 Reboot app을 실행합니다.

로컬에서는 다음 명령으로 실행합니다.

.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
검사 결과
다음 검사를 완료했습니다.

Python 구문 검사 통과

README 43개 메뉴 화면 생성 검사 통과

종목명 일부 검색 검사 통과

자동완성 목록 선택 검사 통과

ETF 이름 검색 검사 통과

개별 종목 조회 검사 통과

특정일 전체 종목 빠른 조회 검사 통과

기간별 전체 종목 반복 조회 검사 통과

대량 조회 실행 버튼 안전장치 검사 통과

Streamlit 서버 기동 확인

실제 전체 종목 기간 조회는 KRX 서버 상태, 로그인 여부, 종목 수와 Streamlit Cloud의 실행 제한에 따라 중간에 종료될 수 있으므로 먼저 일부 종목으로 시험하는 것이 안전합니다.


종목코드 시장명에 "삼성"만 입력했는데 삼성전자나 삼성화재 같은 종목명이 뜨지 않아 다시 수정해줘 그리고 쉬운조회에서 조회 시 아래와 같은 에러 발생하는데 확인해줘

streamlit.errors.StreamlitDuplicateElementKey: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).

Traceback:
File "/mount/src/pykrx/app.py", line 813, in <module>
    render_result()
File "/mount/src/pykrx/app.py", line 236, in render_result
    selected = st.multiselect(
               ^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/streamlit/runtime/metrics_util.py", line 568, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/streamlit/elements/widgets/multiselect.py", line 530, in multiselect
    return self._multiselect(
           ^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/streamlit/elements/widgets/multiselect.py", line 617, in _multiselect
    element_id = compute_and_register_element_id(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.11/site-packages/streamlit/elements/lib/utils.py", line 261, in compute_and_register_element_id
    _register_element_id(ctx, element_type, element_id)
File "/home/adminuser/venv/lib/python3.11/site-packages/streamlit/elements/lib/utils.py", line 143, in _register_element_id
    raise StreamlitDuplicateElementKey(user_key)

4m 55s 동안 처리함
두 문제를 함께 수정했습니다.

원인
1. 삼성을 입력해도 종목이 나오지 않은 이유
현재 Streamlit Cloud에서 실행 중인 app.py는 종목명 자동완성 수정본이 아니라 이전 버전입니다.

오류 로그에서 다음 위치가 확인됩니다.

/mount/src/pykrx/app.py, line 813
render_result()
이전 버전은 종목코드 또는 시장명을 일반 text_input으로만 받아서 삼성을 종목코드처럼 그대로 API에 전달합니다. 따라서 삼성전자·삼성화재 목록이 나타나지 않습니다.

수정본에서는 종목 목록을 다음 순서로 불러옵니다.

PyKRX의 전체 상장 종목 목록

KRX 전 종목 코드·종목명 API

전 종목 가격변동 자료의 종목명

티커 목록과 종목명 조회 함수

검색창에 다음처럼 일부만 입력할 수 있습니다.

삼성
목록 예시:

삼성전자 (005930) · KOSPI
삼성전자우 (005935) · KOSPI
삼성화재 (000810) · KOSPI
삼성화재우 (000815) · KOSPI
삼성SDI (006400) · KOSPI
삼성생명 (032830) · KOSPI
실제 표시되는 종목은 해당 조회일 현재 상장 종목 기준입니다.

2. StreamlitDuplicateElementKey 원인
조회 결과를 쉬운 조회 탭과 전체 API 실행기 탭에서 동시에 렌더링하면서, 두 화면이 다음과 같은 동일한 키를 사용했습니다.

key="result_chart_columns"
Streamlit은 탭이 달라도 한 번의 실행에서 모든 탭 코드를 처리합니다. 따라서 같은 키를 두 번 만나면 중복 키 오류가 납니다.

수정본에서는 다음처럼 탭별 키를 분리했습니다.

key="readme_result_numeric_columns"
key="explorer_result_numeric_columns"
CSV·JSON 다운로드 버튼과 전체 종목 실패 목록 다운로드 버튼도 모두 탭별로 고유한 키를 사용하도록 수정했습니다.

수정된 파일
app.py

전체 수정 파일 ZIP 다운로드

requirements.txt

Secrets 설정 예제

GitHub에 적용하는 방법
GitHub 저장소에서 기존 app.py 일부만 수정하지 말고, 파일 전체를 새 app.py로 교체하세요.

저장소 구조:

pykrx
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── pykrx
    ├── stock
    ├── bond
    └── website
GitHub 웹에서 진행하는 경우:

저장소의 app.py를 엽니다.

연필 모양 Edit this file을 누릅니다.

기존 코드 전체를 삭제합니다.

새 app.py 전체 내용을 붙여 넣습니다.

Commit changes를 누릅니다.

파일 업로드 방식으로 교체해도 됩니다.

Streamlit Cloud 재실행
GitHub 커밋 후 Streamlit Cloud에서 다음 순서로 진행하세요.

Manage app
→ Reboot app
자동 재배포가 시작되면 잠시 후 새 버전이 실행됩니다.

재부팅 후 앱 왼쪽 사이드바에서 다음 버튼을 한 번 누릅니다.

종목 목록 새로고침
기존에 저장된 종목코드 전용 캐시가 남아 있을 수 있기 때문에 새 종목명 목록을 다시 불러오는 과정입니다.

수정 여부 확인 방법
새 파일은 약 2,300줄 정도입니다. GitHub의 app.py가 여전히 약 800줄 정도라면 이전 파일이 남아 있는 것입니다.

새 파일에서는 결과 출력 함수가 다음 형태입니다.

def render_result(namespace: str) -> None:
파일 아래쪽에는 다음 호출이 있어야 합니다.

render_result("readme")
render_result("explorer")
기존처럼 아래 코드가 있으면 이전 버전입니다.

render_result()
검색 시험 방법
앱에서 다음 순서로 선택합니다.

README 전체 기능
→ 2.1.1 MarketData API
→ 2.1.1.2 일자별 OHLCV 조회
→ 개별 종목
종목 이름 검색창에 입력합니다.

삼성
그러면 아래 주식 종목 선택 목록에 삼성 관련 종목들이 표시됩니다.

수정본은 자동 검사에서 다음을 확인했습니다.

삼성 검색 시 삼성전자 (005930) 표시

부분 종목명 검색 정상 작동

종목코드 일부 검색 정상 작동

탭별 결과 차트 키 중복 없음

쉬운 조회 실행 후 StreamlitDuplicateElementKey 없음

전체 종목 조회 화면 정상 생성

Python 구문 검사 통과


이미지 017.png
첨부의 이미지처럼 삼성을 입력해도 자동완성도 되지않고 동일해. 그리고 아래 에러사항도 계속 나와. 해결해줘

5m 23s 동안 처리함
<thinking> 첨부 화면과 현재 GitHub의 실제 `app.py`를 대조했습니다. 화면은 수정본이 아니라 기존 파일을 실행하고 있었고, 기존 코드 안에 자동완성 미구현과 중복 위젯 키 문제가 모두 남아 있었습니다. </thinking> <output>
원인 확인
현재 GitHub 저장소의 app.py는 여전히 843줄짜리 기존 버전입니다. 이 파일은 투자자 수급 화면에서 종목명을 검색하는 것이 아니라 종목코드 또는 시장명을 단순 텍스트로 입력받고 있습니다. 따라서 삼성을 입력하면 삼성전자 검색이 아니라 API에 "삼성"이라는 잘못된 코드가 그대로 전달됩니다. 

또한 동일한 render_result()를 쉬운 조회 탭과 전체 API 실행기 탭에서 모두 실행하면서, 내부의 차트 선택과 CSV 다운로드 위젯에 고유한 key가 없습니다. Streamlit은 화면에 보이지 않는 탭도 함께 실행하므로 StreamlitDuplicateElementKey가 발생합니다. 

즉, 이전 수정 파일이 GitHub의 실제 app.py에 제대로 반영되지 않은 상태였습니다.

수정 파일
이번에는 현재 GitHub에 있는 843줄짜리 app.py를 직접 기준으로 수정했습니다.

app.py

전체 수정 파일 ZIP 다운로드

%EC%88%98%EC%A0%95%EC%82%AC%ED%95%AD_%EC%A0%81%EC%9A%A9%EB%B0%A9%EB%B2%95.txt

수정된 종목 검색 화면
기존 입력란:

종목코드 또는 시장명
[ 삼성                                  ]
수정 후에는 먼저 조회 대상을 선택합니다.

조회 대상

○ 개별 종목
○ 시장 전체
개별 종목을 선택한 경우
종목명 또는 종목코드 일부 입력
[ 삼성                                  ]

종목 검색 결과에서 선택
▼ 삼성전자 (005930) · KOSPI
  삼성화재 (000810) · KOSPI
  삼성전자우 (005935) · KOSPI
  삼성생명 (032830) · KOSPI
삼성, 화재, 하이닉스, 에이피알, 0059처럼 일부만 입력해도 결과가 좁혀집니다.

선택 후에는 다음과 같이 표시됩니다.

선택됨: 삼성화재 · 000810 · KOSPI
시장 전체를 선택한 경우
종목명 검색 대신 시장을 선택합니다.

시장명

KOSPI
KOSDAQ
KONEX
ALL
이렇게 하면 기존처럼 한 입력란에서 종목코드와 시장명을 혼용하지 않습니다.

중복 키 오류 수정
기존에는 두 탭에서 동일한 위젯 키를 사용했습니다.

key="result_chart_columns"
CSV 다운로드 버튼에는 아예 명시적인 키가 없었습니다.

수정본에서는 탭마다 완전히 다른 키를 사용합니다.

key="easy_result_chart_columns"
key="explorer_result_chart_columns"
CSV 다운로드도 분리했습니다.

key="easy_result_csv_download"
key="explorer_result_csv_download"
JSON 다운로드와 API 목록 다운로드에도 모두 고유 키를 부여했습니다.

반드시 파일 전체를 교체해야 합니다
GitHub에서 기존 코드 일부에 덧붙이지 말고, 기존 app.py를 새 파일 전체로 교체해야 합니다.

방법 1: GitHub 파일 업로드로 교체
GitHub 저장소로 들어갑니다.

기존 app.py를 삭제합니다.

Add file → Upload files를 선택합니다.

다운로드한 새 app.py를 업로드합니다.

Commit changes를 누릅니다.

방법 2: GitHub 편집기로 교체
기존 app.py를 엽니다.

연필 모양 Edit this file을 누릅니다.

Ctrl + A로 기존 내용을 전부 선택합니다.

전부 삭제합니다.

새 app.py 전체 내용을 붙여 넣습니다.

Commit changes를 누릅니다.

일부분만 복사하면 기존 render_result()와 새 코드가 함께 남아 다시 중복 오류가 날 수 있습니다.

새 파일이 정확히 올라갔는지 확인
GitHub의 app.py에서 다음 문구를 검색하세요.

APP_VERSION = "2026.07.15-autocomplete-v3"
또한 다음 함수가 있어야 합니다.

def stock_name_selector(
결과 출력 함수도 다음처럼 namespace를 받아야 합니다.

def render_result(namespace: str) -> None:
파일 하단에는 다음 호출이 있어야 합니다.

render_result("easy")
render_result("explorer")
아래처럼 인자가 없는 코드가 남아 있으면 이전 버전입니다.

render_result()
Streamlit Cloud 재배포
GitHub에 커밋한 뒤 Streamlit Cloud에서 다음 순서로 진행합니다.

Manage app
→ Reboot app
재부팅 후 왼쪽 사이드바에 다음 문구가 보여야 합니다.

앱 버전: 2026.07.15-autocomplete-v3
이 문구가 보이지 않으면 새 파일이 실행되지 않은 것입니다.

그 경우 Streamlit Cloud 설정에서 다음을 확인합니다.

Repository: sm86smile/pykrx
Branch: master
Main file path: app.py
새 버전이 표시된 후 사이드바의 다음 버튼을 한 번 누르세요.

종목명 목록 새로고침
검증 결과
수정 파일에 대해 다음을 확인했습니다.

Python 구문 검사 통과

삼성 입력 시 삼성전자·삼성화재 검색 결과 표시

검색 결과에서 삼성화재 선택 가능

선택한 종목코드가 API에 전달됨

쉬운 조회 후 결과 표 정상 출력

쉬운 조회와 전체 API 탭 결과를 동시에 렌더링해도 오류 없음

차트 선택 위젯 중복 없음

CSV 다운로드 버튼 중복 없음

StreamlitDuplicateElementKey 미발생

</output> <reflection> 현재 화면의 가장 중요한 확인 기준은 사이드바의 앱 버전입니다. `2026.07.15-autocomplete-v3`가 표시되지 않는다면 코드 문제가 아니라 GitHub 파일 교체 또는 Streamlit 배포 대상 브랜치·파일 경로가 아직 이전 상태인 것입니다. </reflection>

app.py


"""PyKRX Streamlit 통합 조회 앱.

저장소 루트에서 실행하세요.
    python -m streamlit run app.py

이 앱은 로컬 저장소의 ``pykrx`` 패키지를 우선 사용합니다.
"""

from __future__ import annotations

import contextlib
import inspect
import io
import json
import os
import traceback
from datetime import date, timedelta
from typing import Any, Callable

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Streamlit / 인증 초기화
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PyKRX 통합 조회",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _load_secrets_to_environment() -> None:
    """Streamlit Secrets의 KRX 계정을 환경변수에 반영한다."""
    try:
        krx_id = st.secrets.get("KRX_ID")
        krx_pw = st.secrets.get("KRX_PW")
    except Exception:
        return

    if krx_id:
        os.environ["KRX_ID"] = str(krx_id)
    if krx_pw:
        os.environ["KRX_PW"] = str(krx_pw)


_load_secrets_to_environment()

# pykrx는 import 시 로그인 관련 메시지를 출력할 수 있으므로 UI에서는 숨긴다.
_import_log = io.StringIO()
try:
    with contextlib.redirect_stdout(_import_log), contextlib.redirect_stderr(_import_log):
        from pykrx import bond, stock
except Exception as exc:  # pragma: no cover - 실제 환경의 설치 오류 안내
    st.error("PyKRX를 불러오지 못했습니다.")
    st.code(str(exc))
    st.info("저장소 루트에서 실행했는지와 requirements.txt 설치 여부를 확인하세요.")
    st.stop()


# -----------------------------------------------------------------------------
# 상수 / 설명
# -----------------------------------------------------------------------------
MARKETS = ["KOSPI", "KOSDAQ", "KONEX", "ALL"]
INDEX_MARKETS = ["KOSPI", "KOSDAQ", "KRX", "테마"]
INVESTORS = [
    "금융투자",
    "보험",
    "투신",
    "사모",
    "은행",
    "기타금융",
    "연기금",
    "기관합계",
    "기타법인",
    "개인",
    "외국인",
    "기타외국인",
    "전체",
]
SHORTING_INCLUDE = ["주식", "ETF", "ETN", "ELW", "신주인수권증서및증권", "수익증권"]
BOND_KINDS = [
    "국고채1년",
    "국고채2년",
    "국고채3년",
    "국고채5년",
    "국고채10년",
    "국고채20년",
    "국고채30년",
    "국민주택1종5년",
    "회사채AA",
    "회사채BBB",
    "CD",
]

CATEGORY_RULES = [
    ("영업일·종목", ["business", "ticker_name", "ticker_list", "major_changes"]),
    ("주식 시세·기본지표", ["market_ohlcv", "market_cap", "market_fundamental", "price_change", "exhaustion", "sector"]),
    ("투자자 수급", ["trading_value", "trading_volume", "net_purchases"]),
    ("지수", ["index_"]),
    ("공매도", ["shorting_"]),
    ("ETF·ETN·ELW", ["etf_", "etn_", "elw_", "etx_"]),
    ("선물", ["future_"]),
    ("채권", ["treasury", "bond"]),
]


# -----------------------------------------------------------------------------
# 공통 유틸리티
# -----------------------------------------------------------------------------
def ymd(value: date) -> str:
    return value.strftime("%Y%m%d")


def get_public_functions(module: Any) -> dict[str, Callable[..., Any]]:
    functions: dict[str, Callable[..., Any]] = {}
    for name in dir(module):
        if not name.startswith("get_"):
            continue
        obj = getattr(module, name)
        if callable(obj):
            functions[name] = obj
    return dict(sorted(functions.items()))


STOCK_FUNCTIONS = get_public_functions(stock)
BOND_FUNCTIONS = get_public_functions(bond)


def category_of(function_name: str) -> str:
    for category, keywords in CATEGORY_RULES:
        if any(keyword in function_name for keyword in keywords):
            return category
    return "기타"


def first_doc_line(func: Callable[..., Any]) -> str:
    doc = inspect.getdoc(func) or ""
    for line in doc.splitlines():
        clean = line.strip()
        if clean and clean not in {"Args:", "Returns:"}:
            return clean
    return "설명이 없습니다."


def safe_signature(func: Callable[..., Any]) -> inspect.Signature | None:
    try:
        return inspect.signature(func)
    except (TypeError, ValueError):
        return None


def serializable(value: Any) -> Any:
    if isinstance(value, (date, pd.Timestamp)):
        return value.strftime("%Y%m%d")
    if isinstance(value, set):
        return sorted(value)
    return value


def result_to_dataframe(result: Any) -> pd.DataFrame | None:
    if isinstance(result, pd.DataFrame):
        return result.copy()
    if isinstance(result, pd.Series):
        return result.to_frame()
    if isinstance(result, dict):
        try:
            return pd.DataFrame(result)
        except ValueError:
            return pd.DataFrame(list(result.items()), columns=["항목", "값"])
    if isinstance(result, (list, tuple, set)):
        values = list(result)
        if not values:
            return pd.DataFrame()
        if isinstance(values[0], dict):
            return pd.DataFrame(values)
        return pd.DataFrame({"값": values})
    return None


def store_result(result: Any, title: str, call_text: str) -> None:
    st.session_state["pykrx_result"] = result
    st.session_state["pykrx_result_title"] = title
    st.session_state["pykrx_call_text"] = call_text


def run_call(
    func: Callable[..., Any],
    args: list[Any],
    kwargs: dict[str, Any],
    title: str,
) -> None:
    call_text = f"{func.__name__}(*{args!r}, **{kwargs!r})"
    try:
        with st.spinner("KRX/Naver 데이터를 조회하고 있습니다..."):
            result = func(*args, **kwargs)
        store_result(result, title, call_text)
        st.success("조회가 완료되었습니다.")
    except Exception as exc:
        st.error("조회 중 오류가 발생했습니다.")
        st.code(f"{type(exc).__name__}: {exc}")
        with st.expander("상세 오류 보기"):
            st.code(traceback.format_exc())
        st.info(
            "로그인이 필요한 API라면 `.streamlit/secrets.toml`에 KRX_ID와 KRX_PW를 설정하고, "
            "조회일이 휴일인지 또는 데이터 제공 시점이 지났는지 확인하세요."
        )


def render_result() -> None:
    if "pykrx_result" not in st.session_state:
        return

    result = st.session_state["pykrx_result"]
    title = st.session_state.get("pykrx_result_title", "조회 결과")
    call_text = st.session_state.get("pykrx_call_text", "")

    st.divider()
    st.subheader(title)
    if call_text:
        st.caption(f"실행 함수: `{call_text}`")

    df = result_to_dataframe(result)
    if df is not None:
        metric1, metric2 = st.columns(2)
        metric1.metric("행 수", f"{len(df):,}")
        metric2.metric("열 수", f"{len(df.columns):,}")

        st.dataframe(df, use_container_width=True, height=480)

        numeric_columns = list(df.select_dtypes(include="number").columns)
        if numeric_columns and len(df) > 1:
            with st.expander("차트 보기"):
                selected = st.multiselect(
                    "차트에 표시할 숫자 열",
                    numeric_columns,
                    default=numeric_columns[: min(3, len(numeric_columns))],
                    key="result_chart_columns",
                )
                if selected:
                    st.line_chart(df[selected])

        csv = df.to_csv(index=True, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            data=csv,
            file_name="pykrx_result.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.write(result)
        json_text = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        st.download_button(
            "JSON 다운로드",
            data=json_text.encode("utf-8"),
            file_name="pykrx_result.json",
            mime="application/json",
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
# 쉬운 조회 화면
# -----------------------------------------------------------------------------
def common_date_range(prefix: str, default_days: int = 30) -> tuple[date, date]:
    c1, c2 = st.columns(2)
    start = c1.date_input(
        "시작일",
        value=date.today() - timedelta(days=default_days),
        key=f"{prefix}_from",
    )
    end = c2.date_input("종료일", value=date.today(), key=f"{prefix}_to")
    return start, end


def render_easy_query() -> None:
    category = st.selectbox(
        "기능 분류",
        ["주식", "투자자 수급", "지수", "공매도", "ETF·ETN·ELW", "선물", "채권", "영업일·종목"],
    )

    if category == "주식":
        feature = st.selectbox(
            "조회 기능",
            [
                "종목 기간별 OHLCV",
                "시장 전체 OHLCV",
                "종목 기간별 시가총액",
                "시장 전체 시가총액",
                "종목 기간별 기본지표",
                "시장 전체 기본지표",
                "기간 가격 변동",
                "외국인 보유·한도소진율",
                "시장 업종 분류",
            ],
        )
        if feature == "종목 기간별 OHLCV":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_ohlcv")
            c1, c2 = st.columns(2)
            freq = c1.selectbox("주기", ["d", "m", "y"], format_func=lambda x: {"d": "일", "m": "월", "y": "년"}[x])
            adjusted = c2.checkbox("수정주가 적용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq, "adjusted": adjusted}, feature)

        elif feature == "시장 전체 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 시가총액":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_cap")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 시가총액":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS, index=3)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 기본지표":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_fund")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 기본지표":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "기간 가격 변동":
            start, end = common_date_range("stock_change")
            market = st.selectbox("시장", MARKETS)
            c1, c2 = st.columns(2)
            adjusted = c1.checkbox("수정주가 적용", value=True)
            delist = c2.checkbox("상장폐지 종목 포함", value=False)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market, "adjusted": adjusted, "delist": delist}, feature)

        elif feature == "외국인 보유·한도소진율":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("종목코드", "005930", max_chars=6)
                start, end = common_date_range("foreign_date")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", MARKETS)
                limited = st.checkbox("외국인 보유한도 제한 종목만", value=False)
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_ticker, [ymd(target)], {"market": market, "balance_limit": limited}, feature)

        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_sector_classifications, [ymd(target), market], {}, feature)

    elif category == "투자자 수급":
        feature = st.selectbox(
            "조회 기능",
            ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량", "투자자 순매수 상위종목", "시장 종목별 수급"],
        )
        start, end = common_date_range("trading")
        if feature in ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량"]:
            ticker = st.text_input("종목코드 또는 시장명", "005930", help="종목코드 대신 KOSPI/KOSDAQ/KONEX/ALL을 입력할 수도 있습니다.")
            c1, c2, c3 = st.columns(3)
            etf = c1.checkbox("ETF 포함")
            etn = c2.checkbox("ETN 포함")
            elw = c3.checkbox("ELW 포함")
            if feature in ["일자별 거래대금", "일자별 거래량"]:
                c1, c2, c3 = st.columns(3)
                on = c1.selectbox("구분", ["순매수", "매수", "매도"])
                detail = c2.checkbox("기관 상세")
                freq = c3.selectbox("주기", ["d", "m", "y"])
                func = stock.get_market_trading_value_by_date if feature == "일자별 거래대금" else stock.get_market_trading_volume_by_date
                kwargs = {"etf": etf, "etn": etn, "elw": elw, "on": on, "detail": detail, "freq": freq}
            else:
                func = stock.get_market_trading_value_by_investor if feature == "기간 투자자별 거래대금" else stock.get_market_trading_volume_by_investor
                kwargs = {"etf": etf, "etn": etn, "elw": elw}
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], kwargs, feature)
        else:
            c1, c2 = st.columns(2)
            market = c1.selectbox("시장", MARKETS)
            investor = c2.selectbox("투자자", INVESTORS, index=9)
            func = stock.get_market_net_purchases_of_equities_by_ticker if feature == "투자자 순매수 상위종목" else stock.get_market_trading_value_and_volume_by_ticker
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market, "investor": investor}, feature)

    elif category == "지수":
        feature = st.selectbox("조회 기능", ["지수 목록", "지수 구성종목", "지수 기간별 OHLCV", "시장 전체 지수 OHLCV", "지수 기본지표", "지수 상장정보", "지수 등락률"])
        if feature == "지수 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        elif feature == "지수 구성종목":
            ticker = st.text_input("지수 티커", "1028", help="예: 코스피200 = 1028")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_portfolio_deposit_file, [ticker], {"date": ymd(target), "alternative": True}, feature)
        elif feature == "지수 기간별 OHLCV":
            ticker = st.text_input("지수 티커", "1028")
            start, end = common_date_range("index_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "시장 전체 지수 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 기본지표":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("지수 티커", "1028")
                start, end = common_date_range("index_fund")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 상장정보":
            group = st.selectbox("계열 구분", INDEX_MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_listing_date, [], {"계열구분": group}, feature)
        else:
            start, end = common_date_range("index_change")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ", "KRX"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market}, feature)

    elif category == "공매도":
        feature = st.selectbox(
            "조회 기능",
            ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "시장 공매도 거래량", "시장 공매도 거래대금", "투자자별 공매도 거래량", "투자자별 공매도 거래대금", "공매도 비중 TOP50", "공매도 잔고 TOP50", "종목 공매도 잔고", "시장 공매도 잔고"],
        )
        if feature in ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "종목 공매도 잔고"]:
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("short_ticker")
            func = {
                "종목 공매도 현황": stock.get_shorting_status_by_date,
                "일자별 공매도 거래량": stock.get_shorting_volume_by_date,
                "일자별 공매도 거래대금": stock.get_shorting_value_by_date,
                "종목 공매도 잔고": stock.get_shorting_balance_by_date,
            }[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        elif feature in ["투자자별 공매도 거래량", "투자자별 공매도 거래대금"]:
            start, end = common_date_range("short_investor")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ"])
            func = stock.get_shorting_investor_volume_by_date if "거래량" in feature else stock.get_shorting_investor_value_by_date
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ", "KONEX"])
            include: list[str] | None = None
            if feature in ["시장 공매도 거래량", "시장 공매도 거래대금"]:
                include = st.multiselect("포함 증권", SHORTING_INCLUDE, default=["주식"])
            func = {
                "시장 공매도 거래량": stock.get_shorting_volume_by_ticker,
                "시장 공매도 거래대금": stock.get_shorting_value_by_ticker,
                "공매도 비중 TOP50": stock.get_shorting_volume_top50,
                "공매도 잔고 TOP50": stock.get_shorting_balance_top50,
                "시장 공매도 잔고": stock.get_shorting_balance_by_ticker,
            }[feature]
            kwargs: dict[str, Any] = {"market": market}
            if include is not None:
                kwargs.update({"include": include, "alternative": True})
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(target)], kwargs, feature)

    elif category == "ETF·ETN·ELW":
        feature = st.selectbox("조회 기능", ["ETF 목록", "ETN 목록", "ELW 목록", "ETF/ETN/ELW 통합 목록", "상품명 조회", "ETF ISIN", "ETF 기간별 OHLCV", "ETF 전체 OHLCV", "ETF 기간 등락률", "ETF 구성종목(PDF)", "ETF 괴리율", "ETF 추적오차", "ETF 투자자별 거래"])
        if feature in ["ETF 목록", "ETN 목록", "ELW 목록"]:
            target = st.date_input("기준일", value=date.today())
            func = {"ETF 목록": stock.get_etf_ticker_list, "ETN 목록": stock.get_etn_ticker_list, "ELW 목록": stock.get_elw_ticker_list}[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [], {"date": ymd(target)}, feature)
        elif feature == "ETF/ETN/ELW 통합 목록":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etx_ticker_list, [product], {"date": ymd(target)}, feature)
        elif feature == "상품명 조회":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            ticker = st.text_input("티커", "069500")
            func = {"ETF": stock.get_etf_ticker_name, "ETN": stock.get_etn_ticker_name, "ELW": stock.get_elw_ticker_name}[product]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)
        elif feature == "ETF ISIN":
            ticker = st.text_input("ETF 티커", "069500")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_isin, [ticker], {}, feature)
        elif feature == "ETF 기간별 OHLCV":
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "ETF 전체 OHLCV":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_ticker, [ymd(target)], {}, feature)
        elif feature == "ETF 기간 등락률":
            start, end = common_date_range("etf_change")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_price_change_by_ticker, [ymd(start), ymd(end)], {}, feature)
        elif feature == "ETF 구성종목(PDF)":
            ticker = st.text_input("ETF 티커", "069500")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_portfolio_deposit_file, [ticker], {"date": ymd(target)}, feature)
        elif feature in ["ETF 괴리율", "ETF 추적오차"]:
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_error")
            func = stock.get_etf_price_deviation if feature == "ETF 괴리율" else stock.get_etf_tracking_error
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        else:
            start, end = common_date_range("etf_trade")
            st.caption("세부 오버로드가 복잡하므로 전체 API 실행기에서 원하는 인자를 직접 입력할 수도 있습니다.")
            if st.button("전체 ETF 거래 조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_trading_volume_and_value, [ymd(start), ymd(end)], {}, feature)

    elif category == "선물":
        feature = st.selectbox("조회 기능", ["선물 상품 목록", "선물 상품명", "선물 일자별 OHLCV"])
        if feature == "선물 상품 목록":
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_list, [], {}, feature)
        elif feature == "선물 상품명":
            ticker = st.text_input("선물 티커", "KRDRVFUK2I")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_name, [ticker], {}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            prod = c2.text_input("선물 상품코드", "KRDRVFUK2I")
            alternative = st.checkbox("휴일이면 인접 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ohlcv_by_ticker, [ymd(target), prod], {"alternative": alternative, "prev": True}, feature)

    elif category == "채권":
        mode = st.radio("조회 방식", ["특정일 전체 채권수익률", "특정 채권 기간 수익률"], horizontal=True)
        if mode == "특정일 전체 채권수익률":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(target)], {}, mode)
        else:
            kind = st.selectbox("채권 종류", BOND_KINDS)
            start, end = common_date_range("bond_yield", default_days=90)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(start), ymd(end), kind], {}, mode)

    else:  # 영업일·종목
        feature = st.selectbox("조회 기능", ["인접 영업일", "기간 영업일", "월별 영업일", "시장 종목 목록", "종목명 조회", "기업 주요 변동사항"])
        if feature == "인접 영업일":
            target = st.date_input("기준일", value=date.today())
            prev = st.radio("휴일 처리", [True, False], format_func=lambda x: "이전 영업일" if x else "다음 영업일", horizontal=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_nearest_business_day_in_a_week, [], {"date": ymd(target), "prev": prev}, feature)
        elif feature == "기간 영업일":
            start, end = common_date_range("business_range")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"fromdate": ymd(start), "todate": ymd(end)}, feature)
        elif feature == "월별 영업일":
            c1, c2 = st.columns(2)
            year = c1.number_input("연도", min_value=1980, max_value=2100, value=date.today().year, step=1)
            month = c2.number_input("월", min_value=1, max_value=12, value=date.today().month, step=1)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"year": int(year), "month": int(month)}, feature)
        elif feature == "시장 종목 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        else:
            ticker = st.text_input("종목코드", "005930")
            func = stock.get_market_ticker_name if feature == "종목명 조회" else stock.get_stock_major_changes
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)


# -----------------------------------------------------------------------------
# 전체 API 자동 실행기
# -----------------------------------------------------------------------------
def render_parameter_widget(
    function_name: str,
    parameter: inspect.Parameter,
    key_prefix: str,
) -> tuple[bool, Any]:
    """서명 정보를 바탕으로 Streamlit 입력 위젯을 만든다.

    반환값의 첫 요소는 해당 인자를 실제 호출에 포함할지 여부다.
    """
    name = parameter.name
    default = parameter.default
    required = default is inspect.Parameter.empty
    label = f"{name}{' *' if required else ''}"
    key = f"{key_prefix}_{name}"

    if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
        return False, None

    # 선택적 인자는 사용 여부를 먼저 선택할 수 있다.
    use_value = True
    if not required:
        use_value = st.checkbox(f"{label} 사용", value=True, key=f"{key}_use")
        if not use_value:
            return False, None

    lower = name.lower()
    if lower in {"fromdate", "startdate", "start_dd", "startdd"}:
        return True, ymd(st.date_input(label, value=date.today() - timedelta(days=30), key=key))
    if lower in {"todate", "enddate", "end_dd", "enddd"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower in {"date", "basedate"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower == "market":
        choices = ["ETF", "ETN", "ELW"] if function_name == "get_etx_ticker_list" else MARKETS
        default_value = default if isinstance(default, str) and default in choices else choices[0]
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower in {"계열구분"}:
        return True, st.selectbox(label, INDEX_MARKETS, key=key)
    if lower == "investor":
        default_value = default if isinstance(default, str) and default in INVESTORS else "개인"
        return True, st.selectbox(label, INVESTORS, index=INVESTORS.index(default_value), key=key)
    if lower == "freq":
        choices = ["d", "m", "y"]
        default_value = default if default in choices else "d"
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower == "on":
        return True, st.selectbox(label, ["순매수", "매수", "매도"], key=key)
    if lower == "include":
        return True, st.multiselect(label, SHORTING_INCLUDE, default=["주식"], key=key)
    if lower == "year":
        return True, int(st.number_input(label, 1980, 2100, date.today().year, key=key))
    if lower == "month":
        return True, int(st.number_input(label, 1, 12, date.today().month, key=key))

    annotation = parameter.annotation
    is_bool = isinstance(default, bool) or annotation is bool
    is_int = isinstance(default, int) and not isinstance(default, bool)
    if is_bool:
        return True, st.checkbox(label, value=bool(default) if default is not inspect.Parameter.empty else False, key=key)
    if is_int:
        return True, int(st.number_input(label, value=int(default), step=1, key=key))

    defaults_by_name = {
        "ticker": "005930",
        "prod": "KRDRVFUK2I",
        "bndKindTpCd": "국고채3년",
    }
    initial = defaults_by_name.get(name, "" if required else str(default))
    return True, st.text_input(label, value=initial, key=key)


def render_api_explorer() -> None:
    st.caption("`stock`와 `bond` 모듈에서 이름이 `get_`으로 시작하는 공개 함수를 자동으로 읽어 실행합니다.")
    module_name = st.radio("모듈", ["stock", "bond"], horizontal=True)
    function_map = STOCK_FUNCTIONS if module_name == "stock" else BOND_FUNCTIONS

    categories = sorted({category_of(name) for name in function_map})
    selected_category = st.selectbox("분류", ["전체"] + categories)
    filtered = {
        name: func
        for name, func in function_map.items()
        if selected_category == "전체" or category_of(name) == selected_category
    }
    function_name = st.selectbox("함수", list(filtered))
    func = filtered[function_name]
    signature = safe_signature(func)

    st.info(first_doc_line(func))
    st.code(f"{module_name}.{function_name}{signature or '(...)'}", language="python")

    doc = inspect.getdoc(func)
    if doc:
        with st.expander("함수 전체 설명"):
            st.text(doc)

    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    has_varargs = False

    if signature is not None:
        parameters = list(signature.parameters.values())
        for param in parameters:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                has_varargs = True
                continue
            include, value = render_parameter_widget(function_name, param, f"api_{module_name}_{function_name}")
            if not include:
                continue
            if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD) and param.default is inspect.Parameter.empty:
                args.append(serializable(value))
            else:
                kwargs[param.name] = serializable(value)

    if has_varargs or signature is None:
        st.warning("이 함수는 여러 호출 형식을 지원합니다. 아래 JSON에 위치 인자와 키워드 인자를 직접 입력하세요.")
        args_text = st.text_area("위치 인자 JSON 배열", value="[]", key=f"varargs_{module_name}_{function_name}")
        kwargs_text = st.text_area("키워드 인자 JSON 객체", value="{}", key=f"varkw_{module_name}_{function_name}")
        try:
            args = json.loads(args_text)
            kwargs = json.loads(kwargs_text)
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise ValueError("위치 인자는 배열, 키워드 인자는 객체여야 합니다.")
        except Exception as exc:
            st.error(f"JSON 입력 오류: {exc}")
            return

    if st.button("선택한 API 실행", type="primary", use_container_width=True):
        run_call(func, args, kwargs, f"{module_name}.{function_name}")


# -----------------------------------------------------------------------------
# API 목록
# -----------------------------------------------------------------------------
def render_api_inventory() -> None:
    rows: list[dict[str, Any]] = []
    for module_name, function_map in [("stock", STOCK_FUNCTIONS), ("bond", BOND_FUNCTIONS)]:
        for name, func in function_map.items():
            rows.append(
                {
                    "모듈": module_name,
                    "분류": category_of(name),
                    "함수": name,
                    "호출 형식": str(safe_signature(func) or "동적 인자"),
                    "설명": first_doc_line(func),
                }
            )
    inventory = pd.DataFrame(rows)
    query = st.text_input("함수명 또는 설명 검색")
    if query:
        mask = inventory.astype(str).apply(lambda col: col.str.contains(query, case=False, na=False)).any(axis=1)
        inventory = inventory[mask]
    st.metric("노출된 공개 함수 수", len(inventory))
    st.dataframe(inventory, use_container_width=True, hide_index=True, height=650)
    st.download_button(
        "API 목록 CSV 다운로드",
        inventory.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        "pykrx_api_list.csv",
        "text/csv",
        use_container_width=True,
    )


# -----------------------------------------------------------------------------
# 메인 화면
# -----------------------------------------------------------------------------
st.title("📊 PyKRX 통합 Streamlit 앱")
st.caption("주식·투자자 수급·지수·공매도·ETF/ETN/ELW·선물·채권 기능을 한 화면에서 조회합니다.")

with st.sidebar:
    st.header("실행 상태")
    local_package_path = getattr(stock, "__file__", "확인 불가")
    st.caption(f"PyKRX 위치: `{local_package_path}`")
    has_id = bool(os.getenv("KRX_ID"))
    has_pw = bool(os.getenv("KRX_PW"))
    if has_id and has_pw:
        st.success("KRX 로그인 환경변수 설정됨")
    else:
        st.warning("KRX 로그인 환경변수 미설정")
        st.caption("일부 API는 로그인 없이도 작동하지만, 인증 필요 기능은 실패할 수 있습니다.")
    with st.expander("Secrets 설정 예시"):
        st.code('KRX_ID = "아이디"\nKRX_PW = "비밀번호"', language="toml")
    st.divider()
    st.warning("조회 버튼을 반복해서 누르지 마세요. KRX 서버에서 과도한 호출을 제한할 수 있습니다.")
    if st.button("마지막 결과 지우기", use_container_width=True):
        for key in ["pykrx_result", "pykrx_result_title", "pykrx_call_text"]:
            st.session_state.pop(key, None)
        st.rerun()

main_tab, explorer_tab, inventory_tab, help_tab = st.tabs(
    ["쉬운 조회", "전체 API 실행기", "API 목록", "실행 안내"]
)

with main_tab:
    render_easy_query()
    render_result()

with explorer_tab:
    render_api_explorer()
    render_result()

with inventory_tab:
    render_api_inventory()

with help_tab:
    st.subheader("로컬 실행")
    st.code(
        """py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py""",
        language="powershell",
    )
    st.subheader("권장 폴더 구조")
    st.code(
        """pykrx-master/
├─ app.py
├─ requirements.txt
├─ pyproject.toml
├─ README.md
└─ pykrx/
   ├─ stock/
   ├─ bond/
   └─ website/""",
        language="text",
    )
    st.subheader("로그인이 필요한 경우")
    st.write("저장소 루트에 `.streamlit/secrets.toml` 파일을 만들고 아래처럼 작성하세요.")
    st.code('KRX_ID = "본인의_KRX_아이디"\nKRX_PW = "본인의_KRX_비밀번호"', language="toml")
    st.warning("`secrets.toml`은 GitHub에 올리지 말고 `.gitignore`에 추가하세요.")
app.py


"""PyKRX Streamlit 통합 조회 앱.

저장소 루트에서 실행하세요.
    python -m streamlit run app.py

이 앱은 로컬 저장소의 ``pykrx`` 패키지를 우선 사용합니다.
"""

from __future__ import annotations

import contextlib
import inspect
import io
import json
import os
import traceback
from datetime import date, timedelta
from typing import Any, Callable

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Streamlit / 인증 초기화
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PyKRX 통합 조회",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _load_secrets_to_environment() -> None:
    """Streamlit Secrets의 KRX 계정을 환경변수에 반영한다."""
    try:
        krx_id = st.secrets.get("KRX_ID")
        krx_pw = st.secrets.get("KRX_PW")
    except Exception:
        return

    if krx_id:
        os.environ["KRX_ID"] = str(krx_id)
    if krx_pw:
        os.environ["KRX_PW"] = str(krx_pw)


_load_secrets_to_environment()

# pykrx는 import 시 로그인 관련 메시지를 출력할 수 있으므로 UI에서는 숨긴다.
_import_log = io.StringIO()
try:
    with contextlib.redirect_stdout(_import_log), contextlib.redirect_stderr(_import_log):
        from pykrx import bond, stock
except Exception as exc:  # pragma: no cover - 실제 환경의 설치 오류 안내
    st.error("PyKRX를 불러오지 못했습니다.")
    st.code(str(exc))
    st.info("저장소 루트에서 실행했는지와 requirements.txt 설치 여부를 확인하세요.")
    st.stop()


# -----------------------------------------------------------------------------
# 상수 / 설명
# -----------------------------------------------------------------------------
MARKETS = ["KOSPI", "KOSDAQ", "KONEX", "ALL"]
INDEX_MARKETS = ["KOSPI", "KOSDAQ", "KRX", "테마"]
INVESTORS = [
    "금융투자",
    "보험",
    "투신",
    "사모",
    "은행",
    "기타금융",
    "연기금",
    "기관합계",
    "기타법인",
    "개인",
    "외국인",
    "기타외국인",
    "전체",
]
SHORTING_INCLUDE = ["주식", "ETF", "ETN", "ELW", "신주인수권증서및증권", "수익증권"]
BOND_KINDS = [
    "국고채1년",
    "국고채2년",
    "국고채3년",
    "국고채5년",
    "국고채10년",
    "국고채20년",
    "국고채30년",
    "국민주택1종5년",
    "회사채AA",
    "회사채BBB",
    "CD",
]

CATEGORY_RULES = [
    ("영업일·종목", ["business", "ticker_name", "ticker_list", "major_changes"]),
    ("주식 시세·기본지표", ["market_ohlcv", "market_cap", "market_fundamental", "price_change", "exhaustion", "sector"]),
    ("투자자 수급", ["trading_value", "trading_volume", "net_purchases"]),
    ("지수", ["index_"]),
    ("공매도", ["shorting_"]),
    ("ETF·ETN·ELW", ["etf_", "etn_", "elw_", "etx_"]),
    ("선물", ["future_"]),
    ("채권", ["treasury", "bond"]),
]


# -----------------------------------------------------------------------------
# 공통 유틸리티
# -----------------------------------------------------------------------------
def ymd(value: date) -> str:
    return value.strftime("%Y%m%d")


def get_public_functions(module: Any) -> dict[str, Callable[..., Any]]:
    functions: dict[str, Callable[..., Any]] = {}
    for name in dir(module):
        if not name.startswith("get_"):
            continue
        obj = getattr(module, name)
        if callable(obj):
            functions[name] = obj
    return dict(sorted(functions.items()))


STOCK_FUNCTIONS = get_public_functions(stock)
BOND_FUNCTIONS = get_public_functions(bond)


def category_of(function_name: str) -> str:
    for category, keywords in CATEGORY_RULES:
        if any(keyword in function_name for keyword in keywords):
            return category
    return "기타"


def first_doc_line(func: Callable[..., Any]) -> str:
    doc = inspect.getdoc(func) or ""
    for line in doc.splitlines():
        clean = line.strip()
        if clean and clean not in {"Args:", "Returns:"}:
            return clean
    return "설명이 없습니다."


def safe_signature(func: Callable[..., Any]) -> inspect.Signature | None:
    try:
        return inspect.signature(func)
    except (TypeError, ValueError):
        return None


def serializable(value: Any) -> Any:
    if isinstance(value, (date, pd.Timestamp)):
        return value.strftime("%Y%m%d")
    if isinstance(value, set):
        return sorted(value)
    return value


def result_to_dataframe(result: Any) -> pd.DataFrame | None:
    if isinstance(result, pd.DataFrame):
        return result.copy()
    if isinstance(result, pd.Series):
        return result.to_frame()
    if isinstance(result, dict):
        try:
            return pd.DataFrame(result)
        except ValueError:
            return pd.DataFrame(list(result.items()), columns=["항목", "값"])
    if isinstance(result, (list, tuple, set)):
        values = list(result)
        if not values:
            return pd.DataFrame()
        if isinstance(values[0], dict):
            return pd.DataFrame(values)
        return pd.DataFrame({"값": values})
    return None


def store_result(result: Any, title: str, call_text: str) -> None:
    st.session_state["pykrx_result"] = result
    st.session_state["pykrx_result_title"] = title
    st.session_state["pykrx_call_text"] = call_text


def run_call(
    func: Callable[..., Any],
    args: list[Any],
    kwargs: dict[str, Any],
    title: str,
) -> None:
    call_text = f"{func.__name__}(*{args!r}, **{kwargs!r})"
    try:
        with st.spinner("KRX/Naver 데이터를 조회하고 있습니다..."):
            result = func(*args, **kwargs)
        store_result(result, title, call_text)
        st.success("조회가 완료되었습니다.")
    except Exception as exc:
        st.error("조회 중 오류가 발생했습니다.")
        st.code(f"{type(exc).__name__}: {exc}")
        with st.expander("상세 오류 보기"):
            st.code(traceback.format_exc())
        st.info(
            "로그인이 필요한 API라면 `.streamlit/secrets.toml`에 KRX_ID와 KRX_PW를 설정하고, "
            "조회일이 휴일인지 또는 데이터 제공 시점이 지났는지 확인하세요."
        )


def render_result() -> None:
    if "pykrx_result" not in st.session_state:
        return

    result = st.session_state["pykrx_result"]
    title = st.session_state.get("pykrx_result_title", "조회 결과")
    call_text = st.session_state.get("pykrx_call_text", "")

    st.divider()
    st.subheader(title)
    if call_text:
        st.caption(f"실행 함수: `{call_text}`")

    df = result_to_dataframe(result)
    if df is not None:
        metric1, metric2 = st.columns(2)
        metric1.metric("행 수", f"{len(df):,}")
        metric2.metric("열 수", f"{len(df.columns):,}")

        st.dataframe(df, use_container_width=True, height=480)

        numeric_columns = list(df.select_dtypes(include="number").columns)
        if numeric_columns and len(df) > 1:
            with st.expander("차트 보기"):
                selected = st.multiselect(
                    "차트에 표시할 숫자 열",
                    numeric_columns,
                    default=numeric_columns[: min(3, len(numeric_columns))],
                    key="result_chart_columns",
                )
                if selected:
                    st.line_chart(df[selected])

        csv = df.to_csv(index=True, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            data=csv,
            file_name="pykrx_result.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.write(result)
        json_text = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        st.download_button(
            "JSON 다운로드",
            data=json_text.encode("utf-8"),
            file_name="pykrx_result.json",
            mime="application/json",
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
# 쉬운 조회 화면
# -----------------------------------------------------------------------------
def common_date_range(prefix: str, default_days: int = 30) -> tuple[date, date]:
    c1, c2 = st.columns(2)
    start = c1.date_input(
        "시작일",
        value=date.today() - timedelta(days=default_days),
        key=f"{prefix}_from",
    )
    end = c2.date_input("종료일", value=date.today(), key=f"{prefix}_to")
    return start, end


def render_easy_query() -> None:
    category = st.selectbox(
        "기능 분류",
        ["주식", "투자자 수급", "지수", "공매도", "ETF·ETN·ELW", "선물", "채권", "영업일·종목"],
    )

    if category == "주식":
        feature = st.selectbox(
            "조회 기능",
            [
                "종목 기간별 OHLCV",
                "시장 전체 OHLCV",
                "종목 기간별 시가총액",
                "시장 전체 시가총액",
                "종목 기간별 기본지표",
                "시장 전체 기본지표",
                "기간 가격 변동",
                "외국인 보유·한도소진율",
                "시장 업종 분류",
            ],
        )
        if feature == "종목 기간별 OHLCV":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_ohlcv")
            c1, c2 = st.columns(2)
            freq = c1.selectbox("주기", ["d", "m", "y"], format_func=lambda x: {"d": "일", "m": "월", "y": "년"}[x])
            adjusted = c2.checkbox("수정주가 적용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq, "adjusted": adjusted}, feature)

        elif feature == "시장 전체 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 시가총액":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_cap")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 시가총액":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS, index=3)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 기본지표":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_fund")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 기본지표":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "기간 가격 변동":
            start, end = common_date_range("stock_change")
            market = st.selectbox("시장", MARKETS)
            c1, c2 = st.columns(2)
            adjusted = c1.checkbox("수정주가 적용", value=True)
            delist = c2.checkbox("상장폐지 종목 포함", value=False)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market, "adjusted": adjusted, "delist": delist}, feature)

        elif feature == "외국인 보유·한도소진율":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("종목코드", "005930", max_chars=6)
                start, end = common_date_range("foreign_date")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", MARKETS)
                limited = st.checkbox("외국인 보유한도 제한 종목만", value=False)
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_ticker, [ymd(target)], {"market": market, "balance_limit": limited}, feature)

        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_sector_classifications, [ymd(target), market], {}, feature)

    elif category == "투자자 수급":
        feature = st.selectbox(
            "조회 기능",
            ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량", "투자자 순매수 상위종목", "시장 종목별 수급"],
        )
        start, end = common_date_range("trading")
        if feature in ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량"]:
            ticker = st.text_input("종목코드 또는 시장명", "005930", help="종목코드 대신 KOSPI/KOSDAQ/KONEX/ALL을 입력할 수도 있습니다.")
            c1, c2, c3 = st.columns(3)
            etf = c1.checkbox("ETF 포함")
            etn = c2.checkbox("ETN 포함")
            elw = c3.checkbox("ELW 포함")
            if feature in ["일자별 거래대금", "일자별 거래량"]:
                c1, c2, c3 = st.columns(3)
                on = c1.selectbox("구분", ["순매수", "매수", "매도"])
                detail = c2.checkbox("기관 상세")
                freq = c3.selectbox("주기", ["d", "m", "y"])
                func = stock.get_market_trading_value_by_date if feature == "일자별 거래대금" else stock.get_market_trading_volume_by_date
                kwargs = {"etf": etf, "etn": etn, "elw": elw, "on": on, "detail": detail, "freq": freq}
            else:
                func = stock.get_market_trading_value_by_investor if feature == "기간 투자자별 거래대금" else stock.get_market_trading_volume_by_investor
                kwargs = {"etf": etf, "etn": etn, "elw": elw}
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], kwargs, feature)
        else:
            c1, c2 = st.columns(2)
            market = c1.selectbox("시장", MARKETS)
            investor = c2.selectbox("투자자", INVESTORS, index=9)
            func = stock.get_market_net_purchases_of_equities_by_ticker if feature == "투자자 순매수 상위종목" else stock.get_market_trading_value_and_volume_by_ticker
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market, "investor": investor}, feature)

    elif category == "지수":
        feature = st.selectbox("조회 기능", ["지수 목록", "지수 구성종목", "지수 기간별 OHLCV", "시장 전체 지수 OHLCV", "지수 기본지표", "지수 상장정보", "지수 등락률"])
        if feature == "지수 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        elif feature == "지수 구성종목":
            ticker = st.text_input("지수 티커", "1028", help="예: 코스피200 = 1028")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_portfolio_deposit_file, [ticker], {"date": ymd(target), "alternative": True}, feature)
        elif feature == "지수 기간별 OHLCV":
            ticker = st.text_input("지수 티커", "1028")
            start, end = common_date_range("index_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "시장 전체 지수 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 기본지표":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("지수 티커", "1028")
                start, end = common_date_range("index_fund")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 상장정보":
            group = st.selectbox("계열 구분", INDEX_MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_listing_date, [], {"계열구분": group}, feature)
        else:
            start, end = common_date_range("index_change")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ", "KRX"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market}, feature)

    elif category == "공매도":
        feature = st.selectbox(
            "조회 기능",
            ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "시장 공매도 거래량", "시장 공매도 거래대금", "투자자별 공매도 거래량", "투자자별 공매도 거래대금", "공매도 비중 TOP50", "공매도 잔고 TOP50", "종목 공매도 잔고", "시장 공매도 잔고"],
        )
        if feature in ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "종목 공매도 잔고"]:
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("short_ticker")
            func = {
                "종목 공매도 현황": stock.get_shorting_status_by_date,
                "일자별 공매도 거래량": stock.get_shorting_volume_by_date,
                "일자별 공매도 거래대금": stock.get_shorting_value_by_date,
                "종목 공매도 잔고": stock.get_shorting_balance_by_date,
            }[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        elif feature in ["투자자별 공매도 거래량", "투자자별 공매도 거래대금"]:
            start, end = common_date_range("short_investor")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ"])
            func = stock.get_shorting_investor_volume_by_date if "거래량" in feature else stock.get_shorting_investor_value_by_date
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ", "KONEX"])
            include: list[str] | None = None
            if feature in ["시장 공매도 거래량", "시장 공매도 거래대금"]:
                include = st.multiselect("포함 증권", SHORTING_INCLUDE, default=["주식"])
            func = {
                "시장 공매도 거래량": stock.get_shorting_volume_by_ticker,
                "시장 공매도 거래대금": stock.get_shorting_value_by_ticker,
                "공매도 비중 TOP50": stock.get_shorting_volume_top50,
                "공매도 잔고 TOP50": stock.get_shorting_balance_top50,
                "시장 공매도 잔고": stock.get_shorting_balance_by_ticker,
            }[feature]
            kwargs: dict[str, Any] = {"market": market}
            if include is not None:
                kwargs.update({"include": include, "alternative": True})
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(target)], kwargs, feature)

    elif category == "ETF·ETN·ELW":
        feature = st.selectbox("조회 기능", ["ETF 목록", "ETN 목록", "ELW 목록", "ETF/ETN/ELW 통합 목록", "상품명 조회", "ETF ISIN", "ETF 기간별 OHLCV", "ETF 전체 OHLCV", "ETF 기간 등락률", "ETF 구성종목(PDF)", "ETF 괴리율", "ETF 추적오차", "ETF 투자자별 거래"])
        if feature in ["ETF 목록", "ETN 목록", "ELW 목록"]:
            target = st.date_input("기준일", value=date.today())
            func = {"ETF 목록": stock.get_etf_ticker_list, "ETN 목록": stock.get_etn_ticker_list, "ELW 목록": stock.get_elw_ticker_list}[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [], {"date": ymd(target)}, feature)
        elif feature == "ETF/ETN/ELW 통합 목록":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etx_ticker_list, [product], {"date": ymd(target)}, feature)
        elif feature == "상품명 조회":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            ticker = st.text_input("티커", "069500")
            func = {"ETF": stock.get_etf_ticker_name, "ETN": stock.get_etn_ticker_name, "ELW": stock.get_elw_ticker_name}[product]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)
        elif feature == "ETF ISIN":
            ticker = st.text_input("ETF 티커", "069500")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_isin, [ticker], {}, feature)
        elif feature == "ETF 기간별 OHLCV":
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "ETF 전체 OHLCV":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_ticker, [ymd(target)], {}, feature)
        elif feature == "ETF 기간 등락률":
            start, end = common_date_range("etf_change")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_price_change_by_ticker, [ymd(start), ymd(end)], {}, feature)
        elif feature == "ETF 구성종목(PDF)":
            ticker = st.text_input("ETF 티커", "069500")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_portfolio_deposit_file, [ticker], {"date": ymd(target)}, feature)
        elif feature in ["ETF 괴리율", "ETF 추적오차"]:
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_error")
            func = stock.get_etf_price_deviation if feature == "ETF 괴리율" else stock.get_etf_tracking_error
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        else:
            start, end = common_date_range("etf_trade")
            st.caption("세부 오버로드가 복잡하므로 전체 API 실행기에서 원하는 인자를 직접 입력할 수도 있습니다.")
            if st.button("전체 ETF 거래 조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_trading_volume_and_value, [ymd(start), ymd(end)], {}, feature)

    elif category == "선물":
        feature = st.selectbox("조회 기능", ["선물 상품 목록", "선물 상품명", "선물 일자별 OHLCV"])
        if feature == "선물 상품 목록":
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_list, [], {}, feature)
        elif feature == "선물 상품명":
            ticker = st.text_input("선물 티커", "KRDRVFUK2I")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_name, [ticker], {}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            prod = c2.text_input("선물 상품코드", "KRDRVFUK2I")
            alternative = st.checkbox("휴일이면 인접 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ohlcv_by_ticker, [ymd(target), prod], {"alternative": alternative, "prev": True}, feature)

    elif category == "채권":
        mode = st.radio("조회 방식", ["특정일 전체 채권수익률", "특정 채권 기간 수익률"], horizontal=True)
        if mode == "특정일 전체 채권수익률":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(target)], {}, mode)
        else:
            kind = st.selectbox("채권 종류", BOND_KINDS)
            start, end = common_date_range("bond_yield", default_days=90)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(start), ymd(end), kind], {}, mode)

    else:  # 영업일·종목
        feature = st.selectbox("조회 기능", ["인접 영업일", "기간 영업일", "월별 영업일", "시장 종목 목록", "종목명 조회", "기업 주요 변동사항"])
        if feature == "인접 영업일":
            target = st.date_input("기준일", value=date.today())
            prev = st.radio("휴일 처리", [True, False], format_func=lambda x: "이전 영업일" if x else "다음 영업일", horizontal=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_nearest_business_day_in_a_week, [], {"date": ymd(target), "prev": prev}, feature)
        elif feature == "기간 영업일":
            start, end = common_date_range("business_range")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"fromdate": ymd(start), "todate": ymd(end)}, feature)
        elif feature == "월별 영업일":
            c1, c2 = st.columns(2)
            year = c1.number_input("연도", min_value=1980, max_value=2100, value=date.today().year, step=1)
            month = c2.number_input("월", min_value=1, max_value=12, value=date.today().month, step=1)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"year": int(year), "month": int(month)}, feature)
        elif feature == "시장 종목 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        else:
            ticker = st.text_input("종목코드", "005930")
            func = stock.get_market_ticker_name if feature == "종목명 조회" else stock.get_stock_major_changes
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)


# -----------------------------------------------------------------------------
# 전체 API 자동 실행기
# -----------------------------------------------------------------------------
def render_parameter_widget(
    function_name: str,
    parameter: inspect.Parameter,
    key_prefix: str,
) -> tuple[bool, Any]:
    """서명 정보를 바탕으로 Streamlit 입력 위젯을 만든다.

    반환값의 첫 요소는 해당 인자를 실제 호출에 포함할지 여부다.
    """
    name = parameter.name
    default = parameter.default
    required = default is inspect.Parameter.empty
    label = f"{name}{' *' if required else ''}"
    key = f"{key_prefix}_{name}"

    if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
        return False, None

    # 선택적 인자는 사용 여부를 먼저 선택할 수 있다.
    use_value = True
    if not required:
        use_value = st.checkbox(f"{label} 사용", value=True, key=f"{key}_use")
        if not use_value:
            return False, None

    lower = name.lower()
    if lower in {"fromdate", "startdate", "start_dd", "startdd"}:
        return True, ymd(st.date_input(label, value=date.today() - timedelta(days=30), key=key))
    if lower in {"todate", "enddate", "end_dd", "enddd"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower in {"date", "basedate"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower == "market":
        choices = ["ETF", "ETN", "ELW"] if function_name == "get_etx_ticker_list" else MARKETS
        default_value = default if isinstance(default, str) and default in choices else choices[0]
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower in {"계열구분"}:
        return True, st.selectbox(label, INDEX_MARKETS, key=key)
    if lower == "investor":
        default_value = default if isinstance(default, str) and default in INVESTORS else "개인"
        return True, st.selectbox(label, INVESTORS, index=INVESTORS.index(default_value), key=key)
    if lower == "freq":
        choices = ["d", "m", "y"]
        default_value = default if default in choices else "d"
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower == "on":
        return True, st.selectbox(label, ["순매수", "매수", "매도"], key=key)
    if lower == "include":
        return True, st.multiselect(label, SHORTING_INCLUDE, default=["주식"], key=key)
    if lower == "year":
        return True, int(st.number_input(label, 1980, 2100, date.today().year, key=key))
    if lower == "month":
        return True, int(st.number_input(label, 1, 12, date.today().month, key=key))

    annotation = parameter.annotation
    is_bool = isinstance(default, bool) or annotation is bool
    is_int = isinstance(default, int) and not isinstance(default, bool)
    if is_bool:
        return True, st.checkbox(label, value=bool(default) if default is not inspect.Parameter.empty else False, key=key)
    if is_int:
        return True, int(st.number_input(label, value=int(default), step=1, key=key))

    defaults_by_name = {
        "ticker": "005930",
        "prod": "KRDRVFUK2I",
        "bndKindTpCd": "국고채3년",
    }
    initial = defaults_by_name.get(name, "" if required else str(default))
    return True, st.text_input(label, value=initial, key=key)


def render_api_explorer() -> None:
    st.caption("`stock`와 `bond` 모듈에서 이름이 `get_`으로 시작하는 공개 함수를 자동으로 읽어 실행합니다.")
    module_name = st.radio("모듈", ["stock", "bond"], horizontal=True)
    function_map = STOCK_FUNCTIONS if module_name == "stock" else BOND_FUNCTIONS

    categories = sorted({category_of(name) for name in function_map})
    selected_category = st.selectbox("분류", ["전체"] + categories)
    filtered = {
        name: func
        for name, func in function_map.items()
        if selected_category == "전체" or category_of(name) == selected_category
    }
    function_name = st.selectbox("함수", list(filtered))
    func = filtered[function_name]
    signature = safe_signature(func)

    st.info(first_doc_line(func))
    st.code(f"{module_name}.{function_name}{signature or '(...)'}", language="python")

    doc = inspect.getdoc(func)
    if doc:
        with st.expander("함수 전체 설명"):
            st.text(doc)

    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    has_varargs = False

    if signature is not None:
        parameters = list(signature.parameters.values())
        for param in parameters:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                has_varargs = True
                continue
            include, value = render_parameter_widget(function_name, param, f"api_{module_name}_{function_name}")
            if not include:
                continue
            if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD) and param.default is inspect.Parameter.empty:
                args.append(serializable(value))
            else:
                kwargs[param.name] = serializable(value)

    if has_varargs or signature is None:
        st.warning("이 함수는 여러 호출 형식을 지원합니다. 아래 JSON에 위치 인자와 키워드 인자를 직접 입력하세요.")
        args_text = st.text_area("위치 인자 JSON 배열", value="[]", key=f"varargs_{module_name}_{function_name}")
        kwargs_text = st.text_area("키워드 인자 JSON 객체", value="{}", key=f"varkw_{module_name}_{function_name}")
        try:
            args = json.loads(args_text)
            kwargs = json.loads(kwargs_text)
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise ValueError("위치 인자는 배열, 키워드 인자는 객체여야 합니다.")
        except Exception as exc:
            st.error(f"JSON 입력 오류: {exc}")
            return

    if st.button("선택한 API 실행", type="primary", use_container_width=True):
        run_call(func, args, kwargs, f"{module_name}.{function_name}")


# -----------------------------------------------------------------------------
# API 목록
# -----------------------------------------------------------------------------
def render_api_inventory() -> None:
    rows: list[dict[str, Any]] = []
    for module_name, function_map in [("stock", STOCK_FUNCTIONS), ("bond", BOND_FUNCTIONS)]:
        for name, func in function_map.items():
            rows.append(
                {
                    "모듈": module_name,
                    "분류": category_of(name),
                    "함수": name,
                    "호출 형식": str(safe_signature(func) or "동적 인자"),
                    "설명": first_doc_line(func),
                }
            )
    inventory = pd.DataFrame(rows)
    query = st.text_input("함수명 또는 설명 검색")
    if query:
        mask = inventory.astype(str).apply(lambda col: col.str.contains(query, case=False, na=False)).any(axis=1)
        inventory = inventory[mask]
    st.metric("노출된 공개 함수 수", len(inventory))
    st.dataframe(inventory, use_container_width=True, hide_index=True, height=650)
    st.download_button(
        "API 목록 CSV 다운로드",
        inventory.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        "pykrx_api_list.csv",
        "text/csv",
        use_container_width=True,
    )


# -----------------------------------------------------------------------------
# 메인 화면
# -----------------------------------------------------------------------------
st.title("📊 PyKRX 통합 Streamlit 앱")
st.caption("주식·투자자 수급·지수·공매도·ETF/ETN/ELW·선물·채권 기능을 한 화면에서 조회합니다.")

with st.sidebar:
    st.header("실행 상태")
    local_package_path = getattr(stock, "__file__", "확인 불가")
    st.caption(f"PyKRX 위치: `{local_package_path}`")
    has_id = bool(os.getenv("KRX_ID"))
    has_pw = bool(os.getenv("KRX_PW"))
    if has_id and has_pw:
        st.success("KRX 로그인 환경변수 설정됨")
    else:
        st.warning("KRX 로그인 환경변수 미설정")
        st.caption("일부 API는 로그인 없이도 작동하지만, 인증 필요 기능은 실패할 수 있습니다.")
    with st.expander("Secrets 설정 예시"):
        st.code('KRX_ID = "아이디"\nKRX_PW = "비밀번호"', language="toml")
    st.divider()
    st.warning("조회 버튼을 반복해서 누르지 마세요. KRX 서버에서 과도한 호출을 제한할 수 있습니다.")
    if st.button("마지막 결과 지우기", use_container_width=True):
        for key in ["pykrx_result", "pykrx_result_title", "pykrx_call_text"]:
            st.session_state.pop(key, None)
        st.rerun()

main_tab, explorer_tab, inventory_tab, help_tab = st.tabs(
    ["쉬운 조회", "전체 API 실행기", "API 목록", "실행 안내"]
)

with main_tab:
    render_easy_query()
    render_result()

with explorer_tab:
    render_api_explorer()
    render_result()

with inventory_tab:
    render_api_inventory()

with help_tab:
    st.subheader("로컬 실행")
    st.code(
        """py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py""",
        language="powershell",
    )
    st.subheader("권장 폴더 구조")
    st.code(
        """pykrx-master/
├─ app.py
├─ requirements.txt
├─ pyproject.toml
├─ README.md
└─ pykrx/
   ├─ stock/
   ├─ bond/
   └─ website/""",
        language="text",
    )
    st.subheader("로그인이 필요한 경우")
    st.write("저장소 루트에 `.streamlit/secrets.toml` 파일을 만들고 아래처럼 작성하세요.")
    st.code('KRX_ID = "본인의_KRX_아이디"\nKRX_PW = "본인의_KRX_비밀번호"', language="toml")
    st.warning("`secrets.toml`은 GitHub에 올리지 말고 `.gitignore`에 추가하세요.")