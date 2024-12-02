drop function if exists selectRoles;
delimiter $$

create function selectRoles(set_Role_ID int, set_Role_Name varchar(50), set_Created_At timestamp)
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Role_Name SEPARATOR ', ') into result from Roles where
            Role_ID = ifnull(set_Role_ID, Role_ID) and
            Role_Name = ifnull(set_Role_Name, Role_Name) and
            Created_At = ifnull(set_Created_At, Created_At);
        
        return result;
    end $$

delimiter ;


drop function if exists selectUsers;
delimiter $$

create function selectUsers(set_User_ID int, set_User_Name varchar(50), set_Role_ID int, set_Email varchar(254))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(User_Name SEPARATOR ', ') into result from Users where
            User_ID = ifnull(set_User_ID, User_ID) and
            User_Name = ifnull(set_User_Name, User_Name) and
            Role_ID = ifnull(set_Role_ID, Role_ID) and
            Email = ifnull(set_Email, Email);
            
        return result;
    end $$

delimiter ;


drop function if exists selectProjects;
delimiter $$

create function selectProjects(set_Project_ID int, set_Project_name varchar(100), set_Status ENUM('Planning', 'In Progress', 'Completed', 'On Hold', 'Canceled'))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Project_Name SEPARATOR ', ') into result from Projects where
            Project_ID = ifnull(set_Project_ID, Project_ID) and
            Project_Name = ifnull(set_Project_name, Project_Name) and
            Status = ifnull(set_Status, Status);

        return result;
    end $$

delimiter ;


drop function if exists selectSubproject;
delimiter $$

create function selectSubproject(set_Subproject_ID int, set_Subproject_Name varchar(100))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Subproject_Name SEPARATOR ', ') into result from Subprojects where
            Subproject_ID = ifnull(set_Subproject_ID, Subproject_ID) and
            Subproject_Name = ifnull(set_Subproject_Name, Subproject_Name);
        
        return result;
    end $$

delimiter ;


drop function if exists selectLogs;
delimiter $$

create function selectLogs(set_Log_ID bigint, set_Project_ID int, set_User_ID int, set_Log_Level ENUM('INFO', 'WARNING', 'ERROR', 'DEBUG', 'CRITICAL'))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Log_ID SEPARATOR ', ') into result from Logs where
            Log_ID = ifnull(set_Log_ID, Log_ID) and
            Project_ID = ifnull(set_Project_ID, Project_ID) and
            User_ID = ifnull(set_User_ID, User_ID) and
            Log_Level = ifnull(set_Log_Level, Log_Level);
        
        return result;
    end $$

delimiter ;


drop function if exists selectAuditLogs;
delimiter $$

create function selectAuditLogs(set_Audit_ID bigint, set_User_ID int, set_Action_type varchar(50))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Audit_ID SEPARATOR ', ') into result from AuditLogs where
            Audit_ID = ifnull(set_Audit_ID, Audit_ID) and
            User_ID = ifnull(set_User_ID, User_ID) and
            Action_Type = ifnull(set_Action_type, Action_Type);

        return result;
    end $$

delimiter ;


drop function if exists selectNotifications;
delimiter $$

create function selectNotifications(set_Notification_ID int, set_User_ID int, set_Project_ID int, set_Status ENUM('Unread', 'Read'))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Notification_ID SEPARATOR ', ') into result from Notifications where
            Notification_ID = ifnull(set_Notification_ID, Notification_ID) and
            User_ID = ifnull(set_User_ID, User_ID) and
            Project_ID = ifnull(set_Project_ID, Project_ID) and
            Status = ifnull(set_Status, Status);

        return result;
    end $$

delimiter ;


drop function if exists selectTasks;
delimiter $$

create function selectTasks(set_Task_ID int, set_Project_ID int, set_Assigned_User_ID int, set_Task_Name varchar(100), set_Priority ENUM('Low', 'Medium', 'High', 'Critical'), set_Status ENUM('Not Started', 'In Progress', 'Completed', 'Blocked'))
    returns varchar(1024)
    deterministic
    begin
        declare result varchar(1024);
        select GROUP_CONCAT(Task_ID SEPARATOR ', ') into result from Tasks where
            Task_ID = ifnull(set_Task_ID, Task_ID) and
            Project_ID = ifnull(set_Project_ID, Project_ID) and
            Assigned_User_ID = ifnull(set_Assigned_User_ID, Assigned_User_ID) and
            Task_Name = ifnull(set_Task_Name, Task_Name) and
            Priority = ifnull(set_Priority, Priority) and
            Status = ifnull(set_Status, Status);

        return result;
    end $$

delimiter ;