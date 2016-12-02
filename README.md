# Jmonitor
项目管理，监控，重启，部署

```
'''
API设计实践,以user为例

＃ 添加一个用户;json类型,list[dict]用于扩展
POST /api/users -d [{"user_name":123}] # 创建资源
POST /api/users/actions -d {ids:[id1,id2,...],actions:["touch","rm","ls"]} # 批量执行动作
POST /api/users/id1/{click} -d [{"actions":["touch","rm","ls"]}] # 对特定资源执行动作
return  创建时间,更新时间,ids,状态码

# 批量删除数据;json类型,
DELETE /api/users -d {ids:[id1,id2,...],fields:[field1,field2,...],where:{field1:{">":1,"<":4}}}
DELETE /api/users/{id1} -d {fields:[field1,field2,...],where:{field1:{">":1,"<":4}}},
return  创建时间,更新时间,ids,状态码

# 修改数据;json类型,
PUT /api/users -d {ids:[id1,id2,...],fields:{field1:value1,field2:value2},where:{field1:{">":1,"<":4}}}
PUT /api/users/{id1} -d {fields:{field1:value1,field2:value2},where:{field1:{">":1,"<":4}}}

# 获取所有的,分页的,片段的用户数据
GET /api/users -d {ids:[id1,id2,...],fields:["user_name","passwd"],where:{field1:{">":1,"<":4}},"page":1,"size":2,"skip":3,}
GET /api/users/{id1} -d {fields:["user_name","passwd"],"page":1,"size":2,"skip":3,}





批量修改数据
PUT /api/users -d {user_ids:[user_id1,user_id2,...],data:{"user_name":12345,"passwd":2222}}



'''
```