# Git 처음 시작하기 — LoRR 연구실 프로젝트

**대상:** Git을 처음 접하는 연구실 구성원. Windows PowerShell 사용을 기준으로 작성했습니다. 실행 명령은 저장소 최상위 폴더에서 입력하세요.

## Git은 파일명을 바꾸는 대신 이력을 기록합니다

- `git` = 내 PC에서 파일 변경 이력을 기록하는 도구.
- `GitHub` = Git 저장소를 팀원과 원격으로 공유하는 서비스.
- `commit` = 하나의 의미 있는 변경을 저장하는 스냅샷. `push` 이전에는 GitHub에 안 보입니다.
- `branch` = 다른 사람의 정상 실행 버전을 건드리지 않고 개발하는 작업선.
- `pull request` = 구현 내용을 검토 후 `main`에 합치는 절차.
- `tag` = 특정 commit을 `v0.1.0` 같은 이름으로 표시하는 고정된 버전 지점.

`planner_final2.py`를 새로 만들지 말고 동일한 파일을 수정한 뒤 commit하세요.

## 1. 이 저장소를 처음 GitHub에 업로드

먼저 https://github.com/new 에서 **`lorr-lmapf-benchmark`** 저장소를 만듭니다. 우선 Private을 권장하며, 저장소 생성 과정에서 **README, `.gitignore`, License 생성 옵션은 모두 체크하지 않습니다**. 본 프로젝트에 이미 README와 `.gitignore`가 있습니다. 연구실 조직 저장소에 올리는 경우 아래 URL의 계정명을 조직 이름으로 변경하세요.

현재 프로젝트 ZIP을 `%USERPROFILE%\projects\lorr-lmapf-benchmark`에 압축 해제하세요. ZIP을 다시 GitHub로 업로드하는 것이 아니라, **압축을 푼 폴더 안의 파일들**을 Git으로 관리합니다.

```powershell
cd "$HOME\projects\lorr-lmapf-benchmark"
git --version
# 없다면 https://git-scm.com/downloads/win 에서 Git for Windows 설치

git config --global --get user.name
git config --global --get user.email
# 위 항목이 비어 있는 경우에만 GitHub 설정에서 선택한 표시 이름/커밋 이메일로 등록
# git config --global user.name "YOUR_GITHUB_NAME"
# git config --global user.email "YOUR_GITHUB_COMMIT_EMAIL"
```

실제 테스트 결과가 있는 원래 프로젝트에서 결과를 가져오는 것은 선택적이지만 권장합니다. **다음 명령어는 실제 결과가 존재할 때만 실행**하고, `examples/`에 들어간 JSON에 개인정보나 내부 자료가 없는지 확인하세요.

```powershell
Copy-Item "$HOME\projects\lorr_cpu_4robot_starter\results\basic_4.json" ".\results\basic_4.json"
python scripts\validate_scenario.py
python scripts\summarize_result.py
python scripts\export_example.py
```

이후 Git 로컬 저장소를 생성하고 첫 커밋을 기록합니다.

```powershell
git init -b main
git status --short
# Git이 추적할 파일을 올리기 전 눈으로 확인

git add .
git diff --cached --stat
# 비밀키/개인 경로/대용량 파일/가상환경 파일이 올라가지 않았는지 확인

git commit -m "chore: establish LoRR 4-agent baseline"
git log --oneline -1

git remote add origin https://github.com/JjangYeonseo/lorr-lmapf-benchmark.git
git remote -v
git push -u origin main
```

- `git init`: 현재 폴더에 `.git` 관리 기록을 생성합니다.
- `git add`: 다음 commit에 포함할 변경사항을 선택합니다.
- `git commit`: **내 PC**에 스냅샷을 만듭니다.
- `git push`: **GitHub**로 업로드합니다.

위 원격 주소는 개인 계정 `JjangYeonseo`에 그 이름으로 저장소를 만든 경우에만 사용합니다. GitHub가 인증을 요구하면 브라우저/자격증명 관리자 인증을 진행하세요. `origin already exists`가 뜨면 먼저 `git remote -v`를 확인하고, 잘못된 경우에만 `git remote set-url origin ...`으로 바꾸세요.

처음 업로드 후 저장소의 **Actions** 탭에서 `CPU LoRR smoke` 워크플로가 실제로 통과하는지 확인하세요. **로컬 Docker 실행 성공과 CI 통과는 다른 검증**입니다. CI가 실패하면 로그를 먼저 조사합니다.

## 2. 다음 실험을 별도 브랜치에서 작업

10대 교차로를 예로 들면:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feat/intersection-10

# 이 시점에 코드, 맵, README 등을 수정하고 로컬 테스트 실행
python scripts\validate_scenario.py

git status
git diff
# 변경한 파일만 선택해 기록해도 좋습니다.
git add scenarios scripts docs README.md
git commit -m "feat: add 10-agent intersection scenario"
git push -u origin feat/intersection-10
```

이제 GitHub 저장소 페이지에서 **Compare & pull request**를 클릭하고 실험 목적과 테스트 결과를 적은 뒤 PR을 만듭니다. 다른 팀원이나 본인이 변경사항을 검토하고 CI를 확인한 다음 `main`에 **Merge**합니다. 오류가 있으면 같은 브랜치에서 새 커밋을 추가하세요.

병합 후:

```powershell
git switch main
git pull --ff-only origin main
git branch -d feat/intersection-10
```

알고리즘별 작업 브랜치 예: `feat/pibt-standalone`, `feat/rhcr`, `fix/collision-metrics`, `docs/meeting-brief`.

## 3. 버전 태그는 언제 찍나?

**첫 CI 통과와 정상 실행 확인 후** 아래처럼 `main`의 특정 커밋에 주석 있는 Git 태그를 붙입니다. 태그는 소스 코드의 버전 표시이지 Docker 이미지 버전이나 논문의 성능 평가 결과를 뜻하지 않습니다.

```powershell
git switch main
git pull --ff-only origin main
git tag -a v0.1.0 -m "4-agent LoRR CPU smoke test verified"
git push origin v0.1.0
```

GitHub의 **Releases → Draft a new release**에서 `v0.1.0` 태그를 선택해 릴리스 노트를 작성할 수 있습니다. 태그는 스냅샷 포인터이므로 **이미 공유한 태그를 덮어쓰거나 재사용하지 마세요**. 이후 필요하면 `v0.1.1`, `v0.2.0` 같은 새 태그를 만듭니다.

예시 마일스톤 (버전이 실제로 발행되기 전까지 *계획*):

| 태그 | 기준 |
| --- | --- |
| `v0.1.0` | 4-agent CPU LoRR 빌드·실행·시각화 및 CI 검증 |
| `v0.2.0` | 10-agent 혼잡·병목 시나리오 및 측정 지표 |
| `v0.3.0` | 여러 알고리즘/Seed의 공정한 비교 |

## 4. 매일 자주 쓰는 명령어

```powershell
git status                  # 수정 파일과 현재 브랜치
git diff                    # 아직 커밋하지 않은 수정 내용
git log --oneline --graph --decorate -10  # 최근 기록
git branch -a               # 브랜치 목록
git pull --ff-only          # 현재 브랜치 최신 변경을 안전하게 가져오기
git push                    # 커밋을 GitHub로 업로드
```

**주의:** `git add .` 후 `git status`와 `git diff --cached --stat` 확인을 생략하지 마세요. `.env`, 토큰, 비밀번호, 개인 사진/동영상 원본, 전체 `results/`, `.venv/`, 빌드 산출물은 기본적으로 업로드하지 않습니다. 실수로 비밀정보를 푸시했다면 파일만 삭제해서 끝나지 않고 접근 토큰을 폐기·재발급해야 합니다. `git push --force` 또는 `git reset --hard`는 처음에는 사용하지 않는 것을 추천합니다.

## 5. 같은 프로젝트를 맥북/다른 팀원이 쓰는 경우

GitHub에 올라간 뒤에는 새로운 기기에서 이 저장소를 복제합니다.

```bash
git clone https://github.com/JjangYeonseo/lorr-lmapf-benchmark.git
cd lorr-lmapf-benchmark
docker compose build lorr
docker compose run --rm lorr
python3 scripts/summarize_result.py
```

같은 Git 저장소를 사용한다고 실행 환경까지 자동으로 통일되는 것은 아닙니다. **Docker**, 고정된 LoRR 소스 커밋, CI, README의 설치 안내를 함께 사용합니다. 현재 Docker 베이스 이미지와 `apt` 패키지는 시간이 지나면 달라질 수 있으므로 연구실 공용 릴리스를 확정할 때 base image digest 및 의존성 잠금까지 강화하세요.

참고 문서: https://docs.github.com/ko/get-started/learning-to-code/getting-started-with-git · https://git-scm.com/book/en/v2/Git-Basics-Tagging
