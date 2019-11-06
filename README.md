MeituanSpier

1.使用代理池的方式获取代理ip,
	需要先安装redis,通过flask框架搭建获取平台,通过特定端口获取ip

2.cookies信息
	请求的参数中有两个参数比较亮眼:uuid和_token
	在源码中我们可以找到uuid,所以就剩token是需要关注的了,
	token的生成我们可以通过js去分析,网上也有一些参考:
	token是将一些参数encode，gzip压缩,base64 encode后,url转码后得到的
	token后面是接有=的,说明通过base64加密的可能性极大,我们按照上述说法解析一下
	https://blog.csdn.net/ian852/article/details/88312648

3.发现美食数据在script标签中是有的,网上很多人都选择用ajax接口去分析,又要破解加密参数,舍近求远了
