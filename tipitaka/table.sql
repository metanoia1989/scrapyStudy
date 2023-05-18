create table chapters (
  id serial primary key,
  pid int not null default 0,
  level smallint not null default 1,
  sort smallint not null default 100,
  url varchar(255),
  name_pali varchar(255) not null,
  name_cn varchar(255),
  name_en varchar(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
comment on column chapters.pid is '父ID 默认0';
comment on column chapters.level is '目录等级 1,2,3,4';
comment on column chapters.url is '章节URL';
comment on column chapters.name_pali is '章节名称 巴利文';
comment on column chapters.name_cn is '章节名称 中文';
comment on column chapters.name_en is '章节名称 英文';

create table chapter_content (
  id serial primary key,
  chapter_id int not null,
  html text,
  text_pali text,
  text_cn text,
  text_en text,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
comment on column chapter_content.chapter_id is '章节ID';
comment on column chapter_content.html is '章节原始HTML内容';
comment on column chapter_content.text_pali is '巴利文文本';
comment on column chapter_content.text_cn is '翻译后的中文';
comment on column chapter_content.text_en is '翻译后的英文';