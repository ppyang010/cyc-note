---
Title: "jfinal事务"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags:
  - "jFinal"
Created: "2015-11-24 15:08:29"
Cover: ""
WizGuid: "eaf955c1-c0d0-4a91-ad2b-bbf5d92dfdf8"
WizType: ""
WizLocation: "/工作/工作日记/"
WizDataMd5: "47d96f993885a15f5f82d0abbb39ffe9"
Modified: "2015-11-24 15:08:44"
WizSyncedAt: "2026-08-18 18:48:31"
---

flag=Db.tx(new IAtom()

{

@Override

public boolean run() throws SQLException

{

Tb_Topic topic = getModel(Tb_Topic.class, "topic");

try

{

if (!getPara("topic.id","").equals("")) {

topic.update();

}

else

{

Date date = new Date();

topic.set("datetime", date);

topic.save();

}

}

catch(Exception e)

{

return false;

}

return true;

}

});
