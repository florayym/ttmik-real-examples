# 推送到 GitHub

仓库：git@github.com:florayym/ttmik-real-examples.git

## 首次推送

```bash
cd ttmik-real-examples
git init
git add .
git commit -m "Add L3/L4/L5 grammar notes from 경희대 축제 vlog"
git branch -M main
git remote add origin git@github.com:florayym/ttmik-real-examples.git
git push -u origin main
```

## 以后追加新笔记

每次分析新内容后，把新文件合并进对应的 level 文件夹（已存在的语法点文件就追加新的 `## 来源` 小节），然后：

```bash
git add .
git commit -m "Add LX notes from [来源名]"
git push
```

学习时间线就靠这些 commit 记录，无需在文件里写日期。
