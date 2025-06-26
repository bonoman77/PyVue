# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).





src/
├── assets/              # 이미지, 폰트 등 정적 자산
├── components/          # 재사용 가능한 컴포넌트
│   ├── ui/              # 순수 UI 컴포넌트 (버튼, 입력 필드 등)
│   ├── layout/          # 레이아웃 관련 컴포넌트
│   └── feature/         # 기능 관련 컴포넌트 (TodoList 등)
├── composables/         # 재사용 가능한 컴포지션 함수
├── constants/           # 상수 정의
├── pages/               # 페이지 컴포넌트
├── router/              # 라우터 설정
├── services/            # API 서비스 레이어
│   ├── api.js           # 기본 API 설정
│   └── todoService.js   # Todo 관련 API 호출
├── store/               # Pinia 스토어
│   ├── index.js         # 스토어 설정
│   └── modules/         # 도메인별 스토어 모듈
│       └── todoStore.js # Todo 관련 스토어
├── styles/              # 전역 스타일
│   ├── global.css       # 전역 CSS
│   └── variables.css    # CSS 변수
├── utils/               # 유틸리티 함수
├── App.vue              # 루트 컴포넌트
└── main.js              # 앱 진입점


src/
├── assets/                    # 이미지, 폰트 등 정적 자산
│   ├── images/                # 이미지 파일
│   └── icons/                 # 아이콘 파일
├── components/                # 재사용 가능한 컴포넌트
│   ├── ui/                    # 기본 UI 컴포넌트
│   │   ├── Button.vue         # 버튼 컴포넌트
│   │   ├── Input.vue          # 입력 필드 컴포넌트
│   │   └── Modal.vue          # 모달 컴포넌트
│   ├── layout/                # 레이아웃 컴포넌트
│   │   ├── Header.vue         # 헤더 컴포넌트
│   │   ├── Footer.vue         # 푸터 컴포넌트
│   │   └── Sidebar.vue        # 사이드바 컴포넌트
│   ├── auth/                  # 인증 관련 컴포넌트
│   │   ├── LoginForm.vue      # 로그인 폼
│   │   └── RegisterForm.vue   # 회원가입 폼
│   ├── todo/                  # 할 일 관련 컴포넌트
│   │   ├── TodoList.vue       # 할 일 목록
│   │   ├── TodoItem.vue       # 할 일 항목
│   │   └── TodoForm.vue       # 할 일 추가/수정 폼
│   ├── board/                 # 게시판 관련 컴포넌트
│   │   ├── BoardList.vue      # 게시글 목록
│   │   ├── BoardItem.vue      # 게시글 항목
│   │   └── BoardForm.vue      # 게시글 작성/수정 폼
│   └── video/                 # 영상 관련 컴포넌트
│       ├── VideoPlayer.vue    # 비디오 플레이어
│       └── VideoList.vue      # 비디오 목록
├── composables/               # 재사용 가능한 컴포지션 함수
│   ├── useAuth.js             # 인증 관련 로직
│   ├── usePagination.js       # 페이지네이션 로직
│   └── useForm.js             # 폼 처리 로직
├── constants/                 # 상수 정의
│   ├── routes.js              # 라우트 경로 상수
│   └── api.js                 # API 엔드포인트 상수
├── pages/                     # 페이지 컴포넌트
│   ├── Home.vue               # 메인 페이지
│   ├── auth/                  # 인증 관련 페이지
│   │   ├── Login.vue          # 로그인 페이지
│   │   └── Register.vue       # 회원가입 페이지
│   ├── todos/                 # 할 일 관련 페이지
│   │   ├── index.vue          # 할 일 목록 페이지
│   │   └── [id].vue           # 할 일 상세/수정 페이지
│   ├── board/                 # 게시판 관련 페이지
│   │   ├── index.vue          # 게시글 목록 페이지
│   │   ├── [id].vue           # 게시글 상세 페이지
│   │   └── write.vue          # 게시글 작성 페이지
│   └── video/                 # 영상 관련 페이지
│       ├── index.vue          # 영상 목록 페이지
│       └── [id].vue           # 영상 시청 페이지
├── router/                    # 라우터 설정
│   ├── index.js               # 메인 라우터 설정
│   ├── auth.routes.js         # 인증 관련 라우트
│   ├── todo.routes.js         # 할 일 관련 라우트
│   ├── board.routes.js        # 게시판 관련 라우트
│   └── video.routes.js        # 영상 관련 라우트
├── services/                  # API 서비스 레이어
│   ├── api.js                 # 기본 API 설정
│   ├── authService.js         # 인증 관련 API
│   ├── todoService.js         # 할 일 관련 API
│   ├── boardService.js        # 게시판 관련 API
│   └── videoService.js        # 영상 관련 API
├── store/                     # Pinia 스토어
│   ├── index.js               # 스토어 설정
│   ├── modules/               # 도메인별 스토어 모듈
│   │   ├── authStore.js       # 인증 관련 스토어
│   │   ├── todoStore.js       # 할 일 관련 스토어
│   │   ├── boardStore.js      # 게시판 관련 스토어
│   │   └── videoStore.js      # 영상 관련 스토어
│   └── plugins/               # 스토어 플러그인
│       └── persistedState.js  # 상태 유지 플러그인
├── styles/                    # 전역 스타일
│   ├── global.css             # 전역 CSS
│   └── variables.css          # CSS 변수
├── utils/                     # 유틸리티 함수
│   ├── date.js                # 날짜 관련 유틸리티
│   ├── validation.js          # 유효성 검사 유틸리티
│   └── storage.js             # 로컬 스토리지 유틸리티
├── App.vue                    # 루트 컴포넌트
└── main.js                    # 앱 진입점