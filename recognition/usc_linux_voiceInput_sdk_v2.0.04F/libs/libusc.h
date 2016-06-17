#ifndef _LIBUSC_H_
#define _LIBUSC_H_


// ���������ʽ
#define AUDIO_FORMAT_PCM_16K         "pcm16k"
#define AUDIO_FORMAT_PCM_8K          "pcm8k"
#define AUDIO_FORMAT_AMRNB           "amrnb"

// ʶ������
#define RECOGNITION_FIELD_GENERAL    "general"
#define RECOGNITION_FIELD_POI        "poi"
#define RECOGNITION_FIELD_SONG       "song"
#define RECOGNITION_FIELD_MEDICAL    "medical"
#define RECOGNITION_FIELD_MOVIETV    "movietv"

// ״̬����
#define USC_ENABLE        "true"
#define USC_DISABLED      "false"

#define LANGUAGE_ENGLISH             "english"
#define LANGUAGE_CANTONESE           "cantonese"
#define LANGUAGE_CHINESE             "chinese"


enum {
    // ʶ������
    USC_OK                           = 0,

    // �н������
    USC_RECOGNIZER_PARTIAL_RESULT    = 2,

    // ��⵽������ʼ
    USC_RECOGNIZER_SPEAK_BEGIN       = 100,

    // ��⵽��������
    USC_RECOGNIZER_SPEAK_END         = 101,

    // ����ʧ��
    USC_FATAL_ERROR                  = -70001,

    // ʶ��������
    USC_NO_HANDLE_INPUT              = -70002,

    // ��������
    USC_INVALID_PARAMETERS           = -70003,

	// �������ݸ�ʽ����
    USC_INVALID_INPUT_DATA           = -70004,

	// ��Ȩ��Ч
    USC_EXPIRED_LICENSE              = -80001
};


enum {
    // ����ΪAPP_KEY
    USC_OPT_APP_KEY                  = 9,

    // ����Ϊ�û�ID
    USC_OPT_USER_ID                  = 14,

    // ѡ��ʶ������ 
    USC_OPT_RECOGNITION_FIELD        = 18,

    USC_ASR_ENGINE_PARAMETER	     = 34,
	
    // �������������ʽ
    USC_OPT_INPUT_AUDIO_FORMAT       = 1001,

};

// ����ʶ����
typedef long long USC_HANDLE;

#ifdef WIN32
	#ifdef LIBUSC_EXPORTS
		#ifdef JNI_EXPORTS
			#define USC_API
		#else
			#define USC_API extern "C" __declspec(dllexport)
		#endif
	#else
		#define USC_API extern "C" __declspec(dllimport)
	#endif
#else
	#define USC_API extern "C" __attribute__ ((visibility("default")))
#endif


// ����������ʶ��
USC_API int usc_create_service(USC_HANDLE* handle);

// ����˽����ʶ��
USC_API int usc_create_service_ext(USC_HANDLE* handle, const char* host, const unsigned short port);

// ����VAD��ʱʱ��
USC_API void usc_vad_set_timeout(USC_HANDLE handle, int frontSil,int backSil);

// ����
USC_API int usc_start_recognizer(USC_HANDLE handle);

// ֹͣ
USC_API int usc_stop_recognizer(USC_HANDLE handle);

// ����ʶ��
USC_API int usc_feed_buffer(USC_HANDLE handle, const char* buffer, int len);

// ���ʶ����
USC_API const char* usc_get_result(USC_HANDLE handle);

// �ͷ�ʶ��
USC_API void usc_release_service(USC_HANDLE handle);

// ����ʶ�����
USC_API int usc_set_option(USC_HANDLE handle, int option_id, const char* value);

// ��ȡSDK �汾��
USC_API const char* usc_get_version();

// ��ǰ����˵����ʼλ�ã���λΪ����
USC_API int usc_get_result_begin_time(USC_HANDLE handle);

// ��ǰ����˵��ֹͣλ�ã���λΪ����
USC_API int usc_get_result_end_time(USC_HANDLE handle);

// ��ȡʶ����ز���
USC_API const char * usc_get_option(USC_HANDLE handle, int option_id);

USC_API void usc_clear_option(USC_HANDLE handle, int option_id);

#endif

