create database cts
use cts
select * from employee
select employee.username , mission.id_mission,mission.name_mission,mission.point,mission.state 
from employee, `cts`.`mission` 
 where employee.id_mission = mission.id_mission  and employee.username='nhat'
INSERT INTO `cts`.`employee` 
(`username`, `password`, `email`, `name_employ`, `birthday`, `address`, `gender`, `deparment`, `phonenumber`, `permit`, `point`, `id_mission`)
 VALUES ('thanh', '123', 'ban', 'A', '1999-10-14', 'A', 'Nữ', 'Dev', '44', '0', '440', '1');

select * from mission
INSERT INTO `cts`.`mission`
 (`name_mission`, `startdate`, `enddate`, `point`, `describe`, `state`, `sum_mission`) 
 VALUES ('Da banh', '2021/4/4', '2022/4/4', '50', 'Da banh tip cho tma', 'con', '12');
select * from missionprocess
select mission.id_mission, employee.name_employ, mission.name_mission , mission.point , missionprocess.status  from 
employee, mission, missionprocess
where missionprocess.id_employee=employee.id_employee and missionprocess.id_mission=mission.id_mission 
and  employee.id_employee = 1
INSERT INTO `cts`.`missionprocess`
 (`id_employee`, `id_mission`, `status`)
 VALUES ('1', '1', 'Đang làm');

select * from exchange
INSERT INTO `cts`.`exchange` (`id_gitf`, `name`, `sum_gift`, `point`) VALUES ('1', 'nuoc loc', '12', '50');
