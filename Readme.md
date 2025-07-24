<!-- /api/v1/notification/trigger/ -->
<!-- {
  "event": "new_login",
  "data": {
    "user_id": 1
  }

{
  "event": "new_comment",
  "data": {
    "comment": "This is a sample comment text.",
    "post_id": "123",              
    "author": "UserA",             
    "messages": "Hi.. Mataes"      
  }
}


{
  "event": "weekly_summary",
  "data": {
    "week_start": "2025-07-01",
    "week_end": "2025-07-07",
    "new_comments": 5,
    "new_logins": 2,
    "summary": "You have 5 new comments and 2 logins this week."
  }
}

{
  "event": "new_login",
  "data": {
    "user_id": "7d2675ef-2d29-4a74-893c-979b8af78efb",
    "ip_address": "192.168.1.25",
    "location": "Kathmandu, Nepal",
    "device": "Windows 11 - Chrome"
  }
}

} -->

<!-- http://localhost:8000/api/doc/#/ -->


<!-- Signup API -->
<!-- {
  "email": "alice@example.com",
  "password": "Test@1234",
  "first_name": "Alice",
  "middle_name": "",
  "last_name": "Smith",
  "phone": "+9779800000001"

{
  "email": "bob@example.com",
  "password": "Test@1234",
  "first_name": "Bob",
  "middle_name": "",
  "last_name": "Johnson",
  "phone": "+9779800000002"
}


} -->


<!-- NotificationType Create by default as reuqiement in assigment though out the migration
Created notif type was 'new_login' for specific user , 'weekly summary for all  user','new_comment' this is the
which is created at the intialization of db in the NotifyHUb

 -->
 <!-- Notification Prefences -->

 <!-- 
 Basically Notification Prefences Was Created when the User is created in the system with the default channels
 in_app with each notification type 
 such as user1 is created i have channessin_app,sms,email and notification type is in system avaibales is 
 'new_login','weeky_summary','new_comment'
 so notificatin prefences is created :
 User1-in_app-new_comment
 User1-in_app-web_login
 User1-in_app-weekly_summary
  such as user1-email-new_comment can be changed
  patch /api/v1/notification/preferences/20/
 and api is provided with that user1 can see edit and delete their notification prefences  accordignly
 
  -->

  <!-- Alert /Triggred -->
  <!-- 
  for the new_login for simulation
  endpoint:-  "/api/v1/notifications/trigger/"
  case1:for new_comment (post by user then simulation trigrres)
  payload : 
  {
  "event":"new_comment", 
  "data":{
  "messages":"Hi.. Mataes"
  }


  }
   -->

   <!-- Delevering Noticiation according to the status failuure or send with channgels choosen and the with what
   type oof notificaiton is send accoring for instance new_login,new_comment and weekly_summary -->

   <!--• GET List unread notifications
   • GET /api/v1/notifications/unread/ List unread notifications  provide the all unread notificatoin 

   
   <!-- Read notification one or many at a time with ids in provided format
   {
  "notifications": [
    32,34
  ]
}
   
   
   
   -->
   
<!-- • GET /api/v1/notifications/history/ Full history   --> 

<!-- With the approirate filtering if needed also pagination for larder fetching of data and also if ordering thn alsoo provided -->
<!-- /api/v1/notification/notification/history/?page=1&search=notification -->

<!-- View what are the Notification type available in the System 

api/v1/notification/notification/notifications-type/?ordering=name for better usebality 

 -->

 