from typing import Annotated

from cookit.pyd import model_with_model_config
from nonebot import get_plugin_config
from nonebot.compat import PYDANTIC_V2
from pydantic import AnyHttpUrl, BaseModel, ConfigDict


def alias_generator(x: str):
    return f"ncm_{x}"


model_config: ConfigDict = {"alias_generator": alias_generator}
if PYDANTIC_V2:
    model_config["coerce_numbers_to_str"] = True


@model_with_model_config(model_config)
class ConfigModel(BaseModel):
    # login
    cookie_music_u: str | None = None  # [None] Cookie登录用，Cookie中的MUSIC_U值
    ctcode: int = 86  # [86] 手机号登录用，登录手机区号
    phone: str | None = None  # [无] 手机号登录用，登录手机号
    email: str | None = None  # [无] 邮箱登录用，登录邮箱
    password: str | None = None  # [无] 帐号明文密码，邮箱登录时为邮箱密码
    password_hash: str | None = None  # [无] 帐号密码MD5哈希，邮箱登录时为邮箱密码
    anonymous: bool = False  # [False] 是否强制游客登录

    # ui
    list_limit: int = 20  # [20] 歌曲列表每页的最大数量
    list_font: str | None = None  # [无] 渲染歌曲列表使用的字体
    lrc_empty_line: str | None = "-"  # [-] 填充歌词空行的字符

    # interaction
    auto_resolve: bool = False  # [False] 当用户发送音乐链接时，是否自动解析并发送音乐卡片
    resolve_cool_down: int = 30  # [30] 自动解析同一链接的冷却时间（单位秒）
    resolve_playable_card: bool = False  # [False] 开启自动解析时，是否解析可播放的卡片
    illegal_cmd_finish: bool = False  # [False] 当用户在点歌时输入了非法指令，是否直接退出点歌
    illegal_cmd_limit: int = 3  # [3] 当未启用NCM_ILLEGAL_CMD_FINISH时，用户点歌输入非法指令的次数限制，填0以禁用
    delete_msg: bool = True  # [True] 是否在退出点歌模式后自动撤回歌曲列表与操作提示信息
    delete_msg_delay: tuple[float, float] = (0.5, 2.0)  # [[0.5, 2.0]] 自动撤回消息间隔时间（单位秒）
    info_contains_url: bool = False  # [True] 发送歌曲信息时一并发送URL
    send_media_tip: bool = False  # [False] 发送歌曲文件前，是否提醒用户

    # behavior
    send_as_card: bool = True  # [True] 在支持的平台下，发送歌曲卡片，此行为不受NCM_SEND_MEDIA控制
    ignore_send_card_failure: bool = True  # [True] 当卡片发送出错后，是否忽略出错后发送歌曲文件的回落流程
    send_media: bool = True  # [True] 是否发送歌曲文件，如关闭将始终提示使用命令获取播放链接
    send_media_no_unimsg_fallback: bool = True  # [True] 如存在平台特定的文件发送逻辑，是否禁止回落到通用的UniMessage发送方式
    send_as_file: bool = False  # [False] 默认发送歌曲文件的方式是发送语音，启动此项则修改行为为上传文件
    ob_v11_local_mode: bool = True  # [True] 在OneBot V11适配器下，是否下载歌曲后使用本地文件路径上传歌曲
    ob_v11_ignore_send_file_failure: bool = False  # [False] 在OneBot V11适配器下且以文件形式发送歌曲时，是否禁用出错时回落到语音发送的行为

    # other
    msg_cache_size: int = 1024  # [1024] 缓存所有用户最近一次操作的总计数量
    msg_cache_time: int = 43200  # [43200] 缓存用户最近一次操作的时长（秒）
    resolve_cool_down_cache_size: int = 1024  # [1024] 缓存歌曲解析的冷却时间的总计数量
    card_sign_url: Annotated[str, AnyHttpUrl] | None = None  # [None] 音卡签名地址（与LLOneBot或NapCat共用），填写后将音卡签名工作交给本插件
    card_sign_timeout: int = 5  # [5] 请求音卡签名地址的超时时间
    ffmpeg_executable: str = "ffmpeg"  # [ffmpeg] FFmpeg可执行文件路径，已加入环境变量可不用配置，腾讯系发送语音需要使用
    safe_filename: bool = True  # [False] 是否将歌曲文件名中的非法字符替换掉
    clean_cache_on_startup: bool = False  # [True] 是否在启动时清空歌曲缓存文件夹


config = get_plugin_config(ConfigModel)
