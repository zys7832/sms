insert into school_chengji(kaoshi_id,kaosheng_id,kemu_id,chengji)
select ks.kaoshi_id,ks.kaosheng_id,jh.id,0
 from school_kaosheng as ks inner join auth_user as user inner join school_jiaoxuejihua as jh inner join accounts_banji as bj
   on ks.kaosheng_id = user.id and user.bj_id=bj.id and jh.sknj_id = bj.nj_id
where ks.kaoshi_id=1 and bj.nj_id=1 and jh.ksfsm_id=1;

/*总分表*/
create table zongfen_t(
  id int auto_increment primary key,
  kaoshi_id int not null,
  xuesheng_id int not null,
  zongfen int not null,
  nianzumingci int not null,
  banjimingci int not null
);
/*分数分布表*/
creable fenshufenbu_t(
  kaoshi_id int not null,
  banji_id int not null,
  zongfen int not null,
  renshu int not null
);
/*统计总分*/
insert into zongfen_t(kaoshi_id,xuesheng_id,zongfen,nianzumingci,banjimingci)
select cj.kaoshi_id,cj.kaosheng_id,sum(chengji) as zf,0,0
 from  school_chengji as cj
where cj.kaoshi_id=1
group by kaosheng_id
order by zf desc;

/*生成一次考试的分数分布图*/
insert into fenshufenbu_t(kaoshi_id,banji_id,zongfen,renshu)
select zf.kaoshi_id,bj.id,zongfen,count(*) as renshu
from zongfen_t as zf inner join auth_user as u inner join accounts_banji as bj
  on zf.xuesheng_id=u.id and u.bj_id=bj.id
 where zf.kaoshi_id=1
group by bj.id,zongfen
order by zongfen desc;


/*统计年组排名  班级排名*/
update zongfen_t as zf inner join auth_user as u set nianzumingci=(select ifnull(sum(renshu),0)+1
from fenshufenbu_t where zongfen>zf.zongfen and kaoshi_id=zf.kaoshi_id),
banjimingci = (select ifnull(sum(renshu),0)+1
from fenshufenbu_t where zongfen>zf.zongfen and kaoshi_id=zf.kaoshi_id and u.bj_id=banji_id)
where kaoshi_id=1 and zf.xuesheng_id=u.id;

/*显示总成绩单*/
select u.first_name,bj.bj,
        cj1.chengji as c1,cj2.chengji as c2,cj3.chengji as c3,cj4.chengji as c4,cj5.chengji as c5,cj6.chengji as c6,cj7.chengji as c7,
        zf.zongfen as zf1,zf.banjimingci as bjmc,zf.nianzumingci nzmc
 from auth_user as u inner join accounts_banji as bj inner join 
       school_chengji as cj1 inner join school_chengji as cj2 inner join school_chengji as cj3 inner join school_chengji as cj4 inner join 
       school_chengji as cj5 inner join school_chengji as cj6 inner join school_chengji as cj7 inner join zongfen_t as zf
   on u.bj_id=bj.id and 
      u.id=cj1.kaosheng_id and u.id=cj2.kaosheng_id and u.id=cj3.kaosheng_id and u.id=cj4.kaosheng_id and u.id=cj5.kaosheng_id and u.id=cj6.kaosheng_id and u.id=cj7.kaosheng_id and 
      u.id=zf.xuesheng_id and 
      zf.kaoshi_id=cj1.kaoshi_id and zf.kaoshi_id=cj2.kaoshi_id and zf.kaoshi_id=cj3.kaoshi_id and cj4.kaoshi_id=zf.kaoshi_id and
      cj5.kaoshi_id = zf.kaoshi_id and cj6.kaoshi_id=zf.kaoshi_id and cj7.kaoshi_id=zf.kaoshi_id
where zf.kaoshi_id=1 and cj1.kemu_id=1 and cj2.kemu_id=2 and cj3.kemu_id=3 and cj4.kemu_id=4 and cj5.kemu_id=5 and cj6.kemu_id=6 and cj7.kemu_id=7
order by zf.zongfen desc;

/*[(100,120),(90,99),(80,89),(70,79),(60,69),(40,59),(0,39)]:*/
create table zhiliangfenxi_t(
  kaoshi_id int not null,
  bj_id int not null,
  kemu_id int not null,
  zongrenshu int not null,
  dankezongfen int not null,
  pingjunfen int default 0,
  c100_120 int default 0,
  c90_99 int default 0,
  c80_89 int default 0,
  c70_79 int default 0,
  c60_69 int default 0,
  c40_59 int default 0,
  c00_39 int default 0,
  yiuxiulu float default 0,
  jigelu float default 0,
  chashenglu float default 0
);

insert into zhiliangfenxi_t(kaoshi_id,kemu_id,bj_id,zongrenshu,dankezongfen)
select cj.kaoshi_id,cj.kemu_id,bj.id,count(*) as renshu,sum(chengji)
  from auth_user as u inner join school_chengji as cj inner join accounts_banji as bj
    on cj.kaosheng_id=u.id and u.bj_id=bj.id
group by cj.kemu_id,bj.id;

update zhiliangfenxi_t as fx
    set pingjunfen = round(dankezongfen/zongrenshu),
    yiuxiulu = (select count(*) from school_chengji as cj inner join auth_user as u inner join school_jiaoxuejihua as jh inner join school_kecheng as kc
                    on cj.kaosheng_id=u.id and cj.kemu_id = jh.id and jh.kch_id=kc.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji>=kc.yxfs)/zongrenshu,
    jigelu = (select count(*) from school_chengji as cj inner join auth_user as u inner join school_jiaoxuejihua as jh inner join school_kecheng as kc
                    on cj.kaosheng_id=u.id and cj.kemu_id = jh.id and jh.kch_id=kc.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji>=kc.jgfs)/zongrenshu,
    chashenglu = (select count(*) from school_chengji as cj inner join auth_user as u inner join school_jiaoxuejihua as jh inner join school_kecheng as kc
                    on cj.kaosheng_id=u.id and cj.kemu_id = jh.id and jh.kch_id=kc.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji<=kc.csfs)/zongrenshu,
    c100_120 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 100 and 120),
    c90_99 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 90 and 99),
    c80_89 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 80 and 89),
    c70_79 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 70 and 79),
    c60_69 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 60 and 69),
    c40_59 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 40 and 59),
    c00_39 =(select count(*) from school_chengji as cj inner join auth_user as u
                    on cj.kaosheng_id=u.id
                    where kaoshi_id=fx.kaoshi_id and kemu_id=fx.kemu_id and fx.bj_id=u.bj_id and cj.chengji between 00 and 39)
    where fx.kaoshi_id=1;

select user.id as id,user.first_name as xuesheng,banji.bj as banji,tcj1.chengji as cj1,tcj2.chengji as cj2,tcj3.chengji as cj3,tcj4.chengji as cj4,tcj5.chengji as cj5,tcj6.chengji as cj6,tcj7.chengji as cj7,zf.zongfen,zf.banjimingci,zf.nianzumingci
from auth_user as user inner join accounts_banji as banji inner join zongfen_t as zf inner join school_chengji as tcj1 inner join school_chengji as tcj2 inner join school_chengji as tcj3 inner join school_chengji as tcj4 inner join school_chengji as tcj5 inner join school_chengji as tcj6 inner join school_chengji as tcj7
on user.id=zf.xuesheng_id and user.bj_id=banji.id and zf.xuesheng_id=tcj1.kaosheng_id and zf.kaoshi_id=tcj1.kaoshi_id and tcj1.kemu_id=1 and zf.xuesheng_id=tcj2.kaosheng_id and zf.kaoshi_id=tcj2.kaoshi_id and tcj2.kemu_id=2 and zf.xuesheng_id=tcj3.kaosheng_id and zf.kaoshi_id=tcj3.kaoshi_id and tcj3.kemu_id=3 and zf.xuesheng_id=tcj4.kaosheng_id and zf.kaoshi_id=tcj4.kaoshi_id and tcj4.kemu_id=4 and zf.xuesheng_id=tcj5.kaosheng_id and zf.kaoshi_id=tcj5.kaoshi_id and tcj5.kemu_id=5 and zf.xuesheng_id=tcj6.kaosheng_id and zf.kaoshi_id=tcj6.kaoshi_id and tcj6.kemu_id=6 and zf.xuesheng_id=tcj7.kaosheng_id and zf.kaoshi_id=tcj7.kaoshi_id and tcj7.kemu_id=7
where zf.kaoshi_id=1
order by zf.zongfen limit 10;