from pathlib import Path

from ctypes import (cdll, CFUNCTYPE,
                    c_bool, c_char_p, c_long, c_int,
                    c_void_p, create_string_buffer, byref)


DLL_PATH = Path(__file__).parent.joinpath("FixApi.dll")
APEX = cdll.LoadLibrary(str(DLL_PATH))

REPLY_FUNC = CFUNCTYPE(c_bool, c_long, c_long, c_int)
PUSH_FUNC = CFUNCTYPE(c_bool, c_long, c_long, c_long, c_char_p)
CONN_FUNC = CFUNCTYPE(c_bool, c_long, c_long, c_void_p)


class ApexApi:
    """
    Wrapper for APEX C API.
    """

    def __init__(self):
        """Constructor"""
        self.reply_call_func = REPLY_FUNC(self.on_reply)
        self.push_call_func = PUSH_FUNC(self.on_push)
        self.conn_call_func = CONN_FUNC(self.on_conn)

    def initialize(self):
        """ initialization """
        n = APEX.Fix_Initialize()
        return bool(n)

    def set_app_info(self, name: str, version: str):
        """ setting application information """
        n = APEX.Fix_SetAppInfo(to_bytes(name), to_bytes(version))
        return bool(n)

    def uninitialize(self):
        """ uninstall library """
        n = APEX.Fix_Uninitialize()
        return bool(n)

    def set_default_info(self, user: str, wtfs: str, fbdm: str, dest: str):
        """ set the default information """
        n = APEX.Fix_SetDefaultInfo(
            to_bytes(user),
            to_bytes(wtfs),
            to_bytes(fbdm),
            to_bytes(dest)
        )
        return bool(n)

    def connect(self, address: str, khh: str, pwd: str, timeout: int):
        """ connected transaction """
        conn = APEX.Fix_Connect(
            to_bytes(address),
            to_bytes(khh),
            to_bytes(pwd),
            timeout
        )
        return conn

    def connect_ex(
        self, address: str, khh: str, pwd: str, file_cert: str,
        cert_pwd: str, file_ca: str, procotol: str, verify: bool,
        timeout: int
    ):
        """ connected transaction """
        conn = APEX.Fix_ConnectEx(
            to_bytes(address),
            to_bytes(khh),
            to_bytes(pwd),
            to_bytes(file_cert),
            to_bytes(cert_pwd),
            to_bytes(file_ca),
            to_bytes(procotol),
            verify,
            timeout
        )
        return conn

    def close(self, conn: int):
        """ disconnect """
        n = APEX.Fix_Close(conn)
        return bool(n)

    def allocate_session(self, conn: int):
        """ distribution session """
        sess = APEX.Fix_AllocateSession(conn)
        return sess

    def release_session(self, sess: int):
        """ release the session """
        n = APEX.Fix_ReleaseSession(sess)
        return bool(n)

    def set_timeout(self, sess: int, timeout: int):
        """ set session timeout """
        n = APEX.Fix_SetTimeOut(sess, c_long(timeout))
        return bool(n)

    def set_wtfs(self, sess: int, wtfs: str):
        """ set on commission """
        n = APEX.Fix_SetWTFS(sess, to_bytes(wtfs))
        return bool(n)

    def set_fbdm(self, sess: int, fbdm: str):
        """ settings source sales """
        n = APEX.Fix_SetFBDM(sess, to_bytes(fbdm))
        return bool(n)

    def set_dest_fbdm(self, sess: int, fbdm: str):
        """ set target sales """
        n = APEX.Fix_SetDestFBDM(sess, to_bytes(fbdm))
        return bool(n)

    def set_node(self, sess: int, node: str):
        """ set the service site """
        n = APEX.Fix_SetNode(sess, to_bytes(node))
        return bool(n)

    def set_gydm(self, sess: int, gydm: str):
        """ set teller no. """
        n = APEX.Fix_SetGYDM(sess, to_bytes(gydm))
        return bool(n)

    def create_head(self, sess: int, func: int):
        """ setting session function number """
        n = APEX.Fix_CreateHead(sess, func)
        return bool(n)

    def set_string(self, sess: int, val: str):
        """ setting request data string """
        n = APEX.Fix_SetString(sess, val)
        return bool(n)

    def set_long(self, sess: int, val: int):
        """ shaping setting request data """
        n = APEX.Fix_SetLong(sess, val)
        return bool(n)

    def set_double(self, sess: int, val: float):
        """ float setting request data """
        n = APEX.Fix_SetDouble(sess, val)
        return bool(n)

    def run(self, sess: int):
        """ run """
        n = APEX.Fix_Run(sess)
        return bool(n)

    def async_run(self, sess: int):
        """ asynchronous operation """
        n = APEX.Fix_AsyncRun(sess)
        return bool(n)

    def is_replyed(self, sess: int, msec: int):
        """ whether the response is received """
        n = APEX.Fix_IsReplyed(sess, msec)
        return bool(n)

    def cancel(self, sess: int):
        """ cancel reply waiting """
        n = APEX.Fix_Cancel(sess, sess)
        return bool(n)

    def get_code(self, sess: int):
        """ get error code """
        return APEX.Fix_GetCode(sess)

    def get_err_msg(self, sess: int):
        """ get an error message """
        size = 256
        out = create_string_buffer(b"", size)

        APEX.Fix_GetErrMsg(sess, out, size)
        return out.value

    def get_count(self, sess: int):
        """ gets the number of rows """
        return APEX.Fix_GetCount(sess)

    def get_item(self, sess: int, fid: int, row: int):
        """ gets the string content """
        size = 256
        out = create_string_buffer(b"", size)

        APEX.Fix_GetItem(sess, fid, out, size, row)
        return out.value

    def get_long(self, sess: int, fid: int, row: int):
        """ get plastic content """
        val = APEX.Fix_GetLong(sess, fid, row)
        return val

    def get_double(self, sess: int, fid: int, row: int):
        """ gets float content """
        val = APEX.Fix_GetDouble(sess, fid, row)
        return val

    def get_have_item(self, sess: int, fid: int, row: int):
        """ check specified response data """
        n = APEX.Fix_HaveItem(sess, fid, row)
        return bool(n)

    def set_token(self, sess: int, token: str):
        """ setting service token """
        n = APEX.Fix_SetToken(sess, token)
        return bool(n)

    def get_token(self, sess: int):
        """ get service token """
        size = 256
        out = create_string_buffer(b"", size)

        APEX.Fix_GetToken(sess, out, size)
        return out.value

    def encode(self, data: str):
        """ encryption """
        data = to_bytes(data)
        buf = create_string_buffer(data, 512)
        APEX.Fix_Encode(buf)
        return to_unicode(buf.value)

    def add_backup_svc_addr(self, address: str):
        """ setting service token """
        address = to_bytes(address)
        n = APEX.Fix_AddBackupSvrAddr(address)
        return bool(n)

    def set_conn_event(self, conn: int):
        """ setting a connection state callback """
        n = APEX.Fix_SetConnEvent(conn, self.conn_call_func)
        return bool(n)

    def is_connect(self, conn: int):
        """ check connection status """
        n = APEX.Fix_IsConnect(conn)
        return bool(n)

    def subscribe_by_customer(self, conn: int, svc: int, khh: str, pwd: str):
        """ subscription data """
        func = APEX[108]
        n = func(conn, svc, self.push_call_func,
                 to_bytes(""), to_bytes(khh), to_bytes(pwd))

        return n

    def unsubscribe_by_handle(self, handle: int):
        """ unsubscribe push """
        n = APEX.Fix_UnSubscibeByHandle(handle)
        return bool(n)

    def get_column_count(self, sess: int, row: int):
        """ gets the number of columns """
        return APEX.Fix_GetColumnCount(sess, row)

    def get_val_with_id_by_index(self, sess: int, row: int, col: int):
        """ according to the ranks of the acquired data """
        s = 256
        buf = create_string_buffer(b"", s)
        fid = c_long(0)
        size = c_int(s)

        APEX.Fix_GetValWithIdByIndex(
            sess, row, col, byref(fid), buf, byref(size))
        return fid.value, to_unicode(buf.value)

    def set_system_no(self, sess: int, val: str):
        """ set the system id """
        n = APEX.Fix_SetSystemNo(sess, to_bytes(val))
        return bool(n)

    def set_default_system_no(self, val: str):
        """ set the default number system """
        n = APEX.Fix_SetDefaultSystemNo(to_bytes(val))
        return bool(n)

    def set_auto_reconnect(self, conn: int, reconnect: int):
        """ automatic connection setting """
        n = APEX.Fix_SetAutoReconnect(conn, reconnect)
        return bool(n)

    def get_auto_reconnect(self, conn: int):
        """ get automatic connection status """
        n = APEX.Fix_GetAutoReconnect(conn)
        return bool(n)

    def create_req(self, sess: int, func: int):
        """ create a task """
        n = APEX.Fix_CreateReq(sess, func)
        return bool(n)

    def get_item_buf(self, sess, row):
        """ gets a cached data """
        size = 1024
        outlen = c_int(size)
        buf = create_string_buffer(b"", size)

        APEX.Fix_GetItemBuf(sess, buf, byref(outlen), row)
        return buf

    def set_item(self, sess: int, fid: int, val: str):
        """ setting request content """
        n = APEX.Fix_SetString(sess, fid, to_bytes(val))
        return bool(n)

    def get_last_err_msg(self):
        """ get an error message """
        size = 256
        out = create_string_buffer(b"", size)

        APEX.Fix_GetLastErrMsg(out, size)
        return to_unicode(out.value)

    def reg_reply_call_func(self, sess: int = 0):
        """ register callback function """
        if not sess:
            n = APEX.Fix_RegReplyCallFunc(c_void_p(None), self.reply_call_func)
        else:
            n = APEX.Fix_RegReplyCallFunc(sess, self.reply_call_func)
        return bool(n)

    def on_reply(self, conn: int, sess: int, recv: int):
        """ asynchronous callbacks （ need to inherit ）"""
        return True

    def on_push(self, conn: int, sess: int, sub: int, data: str):
        """ push callback （ need to inherit ）"""
        return True

    def on_conn(self, conn: int, event, recv):
        """ callback connection （ need to inherit ）"""
        return True


def to_bytes(data: str):
    """
     will unicode convert a string bytes
    """
    try:
        bytes_data = data.encode("GBK")
        return bytes_data
    except AttributeError:
        return data


def to_unicode(data: bytes):
    """
     will bytes convert a string unicode
    """
    return data.decode("GBK")
