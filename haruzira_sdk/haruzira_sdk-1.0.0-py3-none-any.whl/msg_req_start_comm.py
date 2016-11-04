# coding: utf-8
import struct
import numpy as np
import haruzirasdk.haruzira_message as haruzira_message

# <summary>
# 通信開始要求メッセージ(0x00)
# </summary>
class MsgReqStartComm(object):

    #region 定数定義
    # <summary>
    # メンバーIndex offset定義
    # </summary>
    __INDEX_ID = 0              #メッセージID
    __INDEX_ENC_FLG = 1         #暗号化フラグ
    __INDEX_CER_FLG = 2         #認証フラグ
    __INDEX_PADDING = 3         #アライメント
    __INDEX_PORT = 4            #ポート番号
    __INDEX_NAME_LEN = 6        #接続元名称サイズ
    __INDEX_PASSWD_LEN = 8      #パスワードサイズ
    __INDEX_PADDING2 = 10       #アライメント
    __INDEX_NAME = 12           #接続元名称
    #endregion

    # <summary>
    # 送信メンバデータ値定義
    # </summary>
    #暗号化フラグ
    __ENC_FLG_OFF = 0x00      #暗号化無
    __ENC_FLG_ON = 0x01       #暗号化有
    #認証フラグ
    __CER_FLG_OFF = 0x00      #認証無
    __CER_FLG_ON = 0x01       #認証有

    def __init__(self):

        self.__id = haruzira_message.MSG_REQ_START_COMM                #メッセージID
        self.__enc_flg = 0x00           #暗号化フラグ
        self.__cer_flg = 0x00             #認証フラグ
        self.__padding = 0x00           #アライメント
        self.__port = 46000            #ポート番号
        self.__name_len = 0x00        #接続元名称サイズ
        self.__passwd_len = 0x00      #パスワードサイズ
        self.__padding2 = 2*[0x00]        #アライメント
        self.__name = None            #接続元名称
        self.__passwd = None          #パスワード
        #self.__byte[] reserve { get; set; }        #予備
        self.__head_len = (1 * 4) + (2 * 3) + len(self.__padding2)                        #ヘッダーサイズ（読み上げデータを除いたサイズ）
        self.__total_len = 0                       #送信フィールド合計サイズ


    #アクセサ定義(メンバーIndex offset)
    def __get_index_id(self):
        return self.__INDEX_ID

    def __get_index_enc_flg(self):
        return self.__INDEX_ENC_FLG

    def __get_index_cer_flg(self):
        return self.__INDEX_CER_FLG

    def __get_index_padding(self):
        return self.__INDEX_PADDING

    def __get_index_port(self):
        return self.__INDEX_PORT

    def __get_index_name_len(self):
        return self.__INDEX_NAME_LEN

    def __get_index_passwd_len(self):
        return self.__INDEX_PASSWD_LEN

    def __get_index_padding2(self):
        return self.__INDEX_PADDING2

    def __get_index_name(self):
        return self.__INDEX_NAME

    #アクセサ定義(送信メンバデータ値)
    def __get_enc_flg_off(self):
        return self.__ENC_FLG_OFF

    def __get_enc_flg_on(self):
        return self.__ENC_FLG_ON

    def __get_cer_flg_off(self):
        return self.__CER_FLG_OFF

    def __get_cer_flg_on(self):
        return self.__CER_FLG_ON

    #アクセサ定義(送信メンバ)
    def __get_id(self):
        return self.__id

    def __get_head_len(self):
        return self.__head_len

    def __get_total_len(self):
        return self.__total_len

    def __get_enc_flg(self):
        return self.__enc_flg

    def __set_enc_flg(self, enc_flg):
        self.__enc_flg = enc_flg

    def __get_cer_flg(self):
        return self.__cer_flg

    def __set_cer_flg(self, cer_flg):
        self.__cer_flg = cer_flg

    def __get_port(self):
        return self.__port

    def __set_port(self, port):
        self.__port = port

    def __get_name_len(self):
        return self.__name_len

    def __set_name_len(self, name_len):
        self.__name_len = name_len

    def __get_passwd_len(self):
        return self.__passwd_len

    def __set_passwd_len(self, passwd_len):
        self.__passwd_len = passwd_len

    def __get_name(self):
        return self.__name

    def __set_name(self, name):
        self.__name = name

    def __get_passwd(self):
        return self.__passwd

    def __set_passwd(self, passwd):
        self.__passwd = passwd


    #Property
    INDEX_ID = property(__get_index_id)
    INDEX_ENC_FLG = property(__get_index_enc_flg)
    INDEX_CER_FLG = property(__get_index_cer_flg)
    INDEX_PADDING = property(__get_index_padding)
    INDEX_PORT = property(__get_index_port)
    INDEX_NAME_LEN = property(__get_index_name_len)
    INDEX_PASSWD_LEN = property(__get_index_passwd_len)
    INDEX_PADDING2 = property(__get_index_padding2)
    INDEX_NAME = property(__get_index_name)
    ENC_FLG_OFF = property(__get_enc_flg_off)
    ENC_FLG_ON = property(__get_enc_flg_on)
    CER_FLG_OFF = property(__get_cer_flg_off)
    CER_FLG_ON = property(__get_cer_flg_on)
    id = property(__get_id)
    head_len = property(__get_head_len)
    total_len = property(__get_total_len)
    enc_flg = property(__get_enc_flg, __set_enc_flg)
    cer_flg = property(__get_cer_flg, __set_cer_flg)
    port = property(__get_port, __set_port)
    name_len = property(__get_name_len, __set_name_len)
    passwd_len = property(__get_passwd_len, __set_passwd_len)
    name = property(__get_name, __set_name)
    passwd = property(__get_passwd, __set_passwd)


    # <summary>
    # 送信データ生成
    # </summary>
    # <returns>生成データサイズ, 生成データ</returns>
    def make_send_data(self):
        self.__total_len = self.head_len + (self.name_len + self.passwd_len)
        data = None

        try:
            #パスワードとアカウント名のチェック
            if self.name_len > 0 and self.name is None:
                return 0, None

            if self.passwd_len > 0 and self.passwd is None:
                return 0, None

            #ネットワークバイトオーダー(little -> big)変換後に、Byte配列に変換
            bPort = struct.unpack("2B", struct.pack(">H", self.port))
            bUserLen = struct.unpack("2B", struct.pack(">H", self.name_len))
            bPasswdLen = struct.unpack("2B", struct.pack(">H", self.passwd_len))

            if self.name is not None and self.passwd is not None:
                data = [self.id] + [self.enc_flg] + [self.cer_flg] + [self.__padding] + list(bPort) + list(bUserLen) + list(bPasswdLen) + list(self.__padding2) + list(self.name) + list(self.passwd)
            else:
                data = [self.id] + [self.enc_flg] + [self.cer_flg] + [self.__padding] + list(bPort) + list(bUserLen) + list(bPasswdLen) + list(self.__padding2)

        except Exception as ex:
            print(ex.args)
            self.__total_len = 0

        return (self.__total_len, data)
