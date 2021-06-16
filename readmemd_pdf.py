import requests,pdfkit,json,time,datetime,os,markdown,re

doneUrl = set()

pdfOptions = {'enable-local-file-access': None}

def convertToPdf(title,url,header,isMarkDown):
  doneUrl.add(url)
  res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=header)
  content = res.text.replace('data-src', 'src')
  # with open(title+'.html', 'w', encoding='utf-8') as f:
  #    f.write(content)
  html=content
  if(isMarkDown):
    html = markdown.markdown(content)

  try:
   pdfkit.from_string(html,'./' + title.replace(' ', '')+'.pdf', options=pdfOptions)
  except Exception as err:
    print(err)

def traverseMenus(pattern,contentStr):
  articleLists = re.findall(pattern,contentStr)
  artictleDict = {}
  i=0
  for s in articleLists:
    if(i > 9991):
      break
    key = re.findall(r'\[.*\]',s)[0]
    key = key.lstrip('[')
    key = key.rstrip(']')
    value = re.findall(r'\(.*\)',s)[0]
    value = value.lstrip('(')
    value = value.rstrip(')')
    artictleDict[key] = value
    i=i+1
    return artictleDict

giteeHeader = {
  #  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

wechatHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
}

wechatPattern = '\[.*\]\(https://mp.weixin.qq.com.*\)'
rootPath = 'https://gitee.com/shishan100/Java-Interview-Advanced/raw/master/'
readmeUrl = rootPath + 'README.md'


response = requests.get(readmeUrl,proxies={'http': None,'https': None},verify=False, headers=giteeHeader)
readmeContent = response.text.replace('data-src', 'src')
html = markdown.markdown(readmeContent)
wechatDict = traverseMenus(wechatPattern,readmeContent)

for key in wechatDict:
  convertToPdf(key,wechatDict[key],wechatHeader,False)




  
