create database cts
use cts

select employee.username , mission.id_mission,mission.name_mission,mission.point,mission.state 
from employee, `cts`.`mission` 
 where employee.id_mission = mission.id_mission  and employee.username='nhat'
INSERT INTO `cts`.`employee` 
(`username`, `password`, `email`, `name_employ`, `birthday`, `address`, `gender`, `deparment`, `phonenumber`, `permit`, `point`, `id_mission`)
 VALUES ('thanh', '123', 'ban', 'A', '1999-10-14', 'A', 'Nữ', 'Dev', '44', '0', '440', '1');

select * from mission;
INSERT INTO `cts`.`mission`
 (`name_mission`, `startdate`, `enddate`, `point`, `describe`, `state`, `sum_mission`) 
 VALUES ('Da banh', '2021/4/4', '2022/4/4', '50', 'Da banh tip cho tma', 'con', '12');
 

select * from missionprocess;



select * from employee;
select missionprocess.id_process, mission.id_mission, mission.name_mission,mission.describe,mission.startdate,mission.enddate , mission.point , 
missionprocess.status    from employee, mission, missionprocess
where missionprocess.id_employee=employee.id_employee and missionprocess.id_mission=mission.id_mission 
and  employee.email = 'ban'

select missionprocess.id_process, mission.id_mission, mission.name_mission
        ,mission.describe,mission.startdate,mission.enddate , mission.point , 
        missionprocess.status  from employee, mission, missionprocess
        where missionprocess.id_employee=employee.id_employee and 
        missionprocess.id_mission=mission.id_mission 
        and employee.email = 'banxavi@gmail.com' 



select * from missionprocess ;
SELECT DISTINCT id_employee,id_mission , status FROM missionprocess where id_employee = 1 and id_mission=4;
select count * from missionprocess;
INSERT INTO missionprocess (id_employee, id_mission, status) VALUES ('1', '2', 'Đang làm');

select * from mission;
UPDATE mission SET sum_mission = sum_mission-1 WHERE id_mission = 1 

INSERT INTO `cts`.`mission` 
(`name_mission`, `startdate`, `enddate`, `point`, `describe`, `state`, `sum_mission`) 
VALUES ('Ngu', '2021-1-1', '2022-1-1', '22', 'an com', 'CON', '22');

select sum(id_mission) from mission

INSERT INTO missionprocess
 (id_employee, id_mission, status)
 VALUES ('2', '1', 'Hoàn thành')

 UPDATE `cts`.`missionprocess` SET `status` = 'Đang làm' WHERE (`id_process` = '4');
 UPDATE `cts`.`missionprocess` SET `status` = 'Đang làm' WHERE (`id_process` = '1');

UPDATE `cts`.`missionprocess` SET `status` = 'Đang làm' WHERE (`id_process` = '6');
UPDATE `cts`.`missionprocess` SET `status` = 'Đang làm' WHERE (`id_process` = '7');
select * from exchange
INSERT INTO `cts`.`exchange` (`id_gitf`, `name`, `sum_gift`, `point`) VALUES ('1', 'nuoc loc', '12', '50');
