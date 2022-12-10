# WoZaiXiaoYuanPuncher-Actions

## 声明

- 本项目fork自[jimlee2002/Actions-WoZaiXiaoYuanPuncher: 我在校园自动打卡程序：WoZaiXiaoYuanPuncher 的 Github Action 版。](https://github.com/jimlee2002/Actions-WoZaiXiaoYuanPuncher)，因为不太熟悉git的操作，故下载jimlee2002的源代码并按自己的需求对代码进行修改并上传，仅为了方便自己和同学使用。
- 现在我在校园用的是QQ地图，不知道以前在哪儿听到说用的是高德地图

## 关于本脚本

- 
- 脚本 `wzxy-healthcheck.py`，对应打卡项目“健康打卡”（一天只需打卡一次，仅需提交位置信息。
- 利用 [actions/cache@v2](https://github.com/marketplace/actions/cache) 实现缓存 jwsession，避免频繁登录可能导致的账号登录问题。
- 利用 Github Action 的 [Secrets](https://docs.github.com/cn/actions/reference/encrypted-Secrets) 加密储存所有配置信息，任何人都无法从项目仓库中直接读取这些敏感信息。
- 支持多用户/多地点打卡，利用 Github Action 的 [Environment](https://docs.github.com/cn/actions/reference/environments) 实现多配置文件的储存。

## 使用指南

### Step0 准备工作

- 在小程序 `我的-设置` 中修改自己的密码。
  - 注意：密码为6-12位
  - 修改密码后，先点击下方的清除缓存，再退出登录
  > 参考[issues#58](https://github.com/jimlee2002/Actions-WoZaiXiaoYuanPuncher/issues/58)

### Step1 Fork本仓库

![step1.1](https://i.loli.net/2021/08/07/CXA4LBzFKxpkYj8.png)

- 点击本仓库页面中右上角的 `Fork` 按钮。

- 稍等片刻，将自动跳转至新建的仓库。

### Step2 配置打卡参数

> 如需配置多用户，请参考文末“其他需求”中的介绍。

- 在新建的仓库页面，点击选项 `Settings`，进入项目仓库设置页面。

- 在左方侧边栏点击选项 `Environments`，点击右上角按钮 `New environment` 创建用于存放用户配置的 Environment，命名为 `WZXY_CONFIG_01`。

![step2.1](https://i.loli.net/2021/08/07/jPYLRtgVk27KAUl.png)

- 进入新建的 Environment ，在 “Environment Secrets” 一栏中点击 `Add Secret` 按钮，根据需要新建下列的 Secret，并填写对应 Value 值：
  <details>
  <summary><b>基本参数</b></summary>

  - `USERNAME`：我在校园账号的用户名。

  - `PASSWORD`：我在校园账号的密码。

  - `CACHE_NAME`：值任意，用于储存 jwsession 的缓存文件的前缀名。为避免信息泄露，建议使用包含数字与大小写英文的无序字符串，且长度在32位以上（可以尝试键盘乱打 or 使用生成器）。
    
    > 请注意：配置多账户打卡时，不同环境中的`CACHE_NAME`不能相同！！
    
  - `CITY`：打卡该项目时所提交位置信息的城市名。
  
  - `ADDRESS_RECOMMEND`：打卡时所提交位置信息的学校名/地点名。
  
    **⚠注意：** 请填写[腾讯地图服务 - 地图坐标拾取器](https://lbs.qq.com/getPoint/)中检索到的学校名/地点名
  
    示例：
    ![image.png](https://s2.loli.net/2022/10/23/gxyQenF1uWYithb.png)


    > 如需两个打卡项目提交不同的地理位置信息（如“日检日报”在校打卡，“健康打卡”在家打卡），请参考文末“常见问题 - 3.如何配置多账户/多地点打卡？” 

  - ~~`ANSWERS`（可选）：打卡时所提交的选项回答，对应抓包信息中的“answers”。可以通过该 Secrect 自定义打卡问题的选项或回答。~~
    
    > ⚠自定义`ANSWERS`功能存在问题，暂时取消该功能，后续修复后将重新上线。
    > 如需自定义打卡时提交的"answers"，请参考代码中的注释，自行修改脚本中的对应字段。


  </details>

  <details>
  <summary><b>钉钉机器人推送服务</b></summary>

  如不创建推送方式对应的 Secret，则不会推送打卡结果通知。

  <details>
  <summary><b>钉钉机器人</b></summary>
  - `DD_BOT_ACCESS_TOKEN`（可选）：钉钉机器人推送 Token，填写机器人的 Webhook 地址中的 token。只需 `https://oapi.dingtalk.com/robot/send?access_token=XXX` 等于=符号后面的XXX即可。

  - `DD_BOT_SECRET`（可选）：钉钉机器人推送SECRET。[官方文档](https://developers.dingtalk.com/document/app/custom-robot-access)

    > 如需配置钉钉机器人，上述的 `DD_BOT_ACCESS_TOKEN` 和 `DD_BOT_SECRET` 两条 Secrect 都需创建。

  </details>

### Step3 配置脚本运行时间 

脚本的触发运行时间由项目仓库内`.github/workflows`的两个 Workflow 文件配置：

- `wzxy_dailyreport.yml`

  - 对应脚本“`wzxy-dailyreport.py`”（打卡项目“日检日报”）。

  - 默认在每天北京时间 7:30 执行。

- `wzxy_healthcheck.yml`

  - 对应脚本“`wzxy-healthcheck.py`”（打卡项目“健康打卡”）。

  - 默认在每天北京时间 0:30 执行。

如果需要修改脚本的运行时间：

![step3.1](https://i.loli.net/2021/08/07/dNeS2igbwKmPzCO.png)

- 点击页面上方选项 `Code`，回到项目仓库主页。

- 点击文件夹`.github/workflows`，修改所需要的 Workflow 文件。

  以修改`wzxy_dailyreport.yml`为例：

  - 点击`wzxy_dailyreport.yml`，进入文件预览。

  - 点击预览界面右上方笔的图标，进入编辑界面。

    ![step3.2](https://i.loli.net/2021/08/07/mvgOB824MsdZ1up.png)

  - 根据自己的打卡时间需要，修改代码中的 cron 表达式：
    > cron是个啥？百度一下！

    ![step3.3](https://i.loli.net/2021/08/07/ntImHFAeu6TM7zK.png)

    > **定时注意事项：**
    >
    > - Github Actions 用的是世界标准时间（UTC），北京时间（UTC+8）转换为世界标准时需要减去8小时。
    > - Github Action 执行计划任务需要排队，脚本并不会准时运行，大概会延迟1h左右，请注意规划时间。

- 修改完成后，点击页面右侧绿色按钮 `Start commit`，然后点击绿色按钮 `Commit changes`。

  > **注意：**
  >
  > 出于开发者个人使用需要，`wzxy_healthcheck.yml`里设定的`environment`参数默认为`environment: WZXY_CONFIG_02`；
  >
  > 如果你严格按照上述教程操作且没有多账户/多地点打卡需要，请找到该行代码并将02改为01。
  >
  > 关于多账户/多配置文件的设置，请参考文末“常见问题”

### Step4 手动测试脚本运行

- 点击页面上方选项 `Actions`，进入 Github Actions 配置页面。

- 左侧边栏点击需要测试的脚本：
  - `WZXY_DailyReport`：对应脚本“`wzxy-dailyreport.py`”，打卡项目“日检日报”。
  - `WZXY_HealthCheck`：对应脚本“`wzxy-healthcheck.py`”，打卡项目“健康打卡”。

以测试 `WZXY_DailyReport` 为例：

![step4.1](https://i.loli.net/2021/08/07/qWERC7NUDuvxPd2.png)

- 在未自行打卡的打卡时段，点击右侧按钮 `Run workflow`，再次点击绿色按钮 `Run workflow`。

- 等待几秒后刷新页面。

- 2分钟后登入我在校园小程序查看。如果一切正常，打卡将被完成。

- 如果正确配置了推送服务，将同时能够收到脚本的推送通知。

- 如果出现以下情况：
  - 2分钟后仍未自动打卡。
  - Github Actions 界面最新的 workflow run `WZXY_HealthCheck` 状态为红色错误。
  - 以及其他错误情况。

  请在Github Actions 配置界面中，打开最新的 Workflow run `WZXY_HealthCheck`，查看错误日志，并检查自己的参数配置是否正确。

下图为脚本正常运行时，Github Action 的日志输出： 
![正常打卡](https://s2.loli.net/2022/10/17/upf6tngqr8AolUL.png)

> 两个脚本对应的 Workflow 都默认开启定时执行任务，如果你无需使用/需要暂时停用某一脚本，请参照以下步骤停用其对应的 Workflow：
>
> ![step4.2](https://i.loli.net/2021/08/07/W23K7Gqzsra59Xf.png)
>
> - 在 Github Actions 配置页面中，左侧边栏选择需要停用的脚本所对应的 Workflow。
> - 点击搜索栏右边的 `...` 按钮，然后点击 `Disable workflow`。

## 常见问题

1. 即便所配置的密码正确，脚本执行时仍然提示`用户名或密码错误，还可尝试*次`？
   - 在小程序中重新修改密码。密码建议使用简单纯数字/纯英文，且不超过10位。
   - 修改完密码后，在小程序上点击清除缓存，然后点击退出登陆，注意先不要在小程序上重新登陆。
   - 更新对应用户配置文件中的 Secret `PASSWORD`，填写新密码。
   - 再次尝试运行脚本，查看是否正常登陆并获取 jwsession。
   - 如果仍然失败，请暂时停用Github Action，冷却一天后再重新尝试。
   - 如仍有问题，请在确保配置文件中密码信息正确的后提 issue。
2. 日检日报提交的选项不对？/ 提示`服务出错(500)`？
   - ~~请参照 Step2 中的介绍，创建并填写 Secrect `ANSWERS`。~~
   - 需要自定义打卡时提交的"answers"。请参考代码中的注释，自行修改脚本中的对应字段。
3. 如何配置多账户/多地点打卡？
   - 参照 Step 2，新建并配置另一环境；环境名建议保持 `WZXY_CONFIG_**`的格式。
   - 参考 Step 3，打开打卡脚本所对应的 workflow 文件，复制末尾的多账户配置示例代码，注销注释后填写另一配置的环境名即可。
4. 打卡不准时？
   - Github Action服务器使用的时间是UTC，设置定时时请注意转换为北京时间（UTC+8）。
   - Github Action执行计划任务需要排队，并不会准时运行脚本，大概会延迟1h左右，请注意规划时间。

## 给自己说的话

- 本脚本只适用于建大雁塔校区研究生，若为雁塔校区博士，请将answer改为[“0”,“2”,“0”]

- 用地方名的原理：

```
令ADDRESS=CITY+ADDRESS_RECOMMEND

首先去访问‘’‘https://apis.map.qq.com/ws/geocoder/v1/?address=ADDRESS&key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR’‘’获取这个地方的经纬度，但是结果中不含有街道信息以及经纬度不够精细，不符合作为我在校园的请求体内容，所以再次用得到的经纬度去‘’‘https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location=纬度,经度’‘’反求街道信息

举例：
https://apis.map.qq.com/ws/geocoder/v1/?address=西安市西安建筑科技大学北院-2号学生公寓&key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR
得到经度108.966316纬度34.237679
https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location=34.237679,108.966316

因此每次新增一个地方的时候都可以在https://lbs.qq.com/getPoint/找到地方的具体名称，再用‘’‘https://apis.map.qq.com/ws/geocoder/v1/?address=ADDRESS&key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR’‘’去查经纬度，再用‘’‘https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location=纬度,经度’‘’来看地方对不对,以防地址弄错
```

