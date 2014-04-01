INSERT INTO auth_user (
	"ID",
	"PASSWORD",
	"LAST_LOGIN",
	"IS_SUPERUSER",
	"ROLE_ID",
	"USERNAME",
	"NAME",
	"EMAIL",
	"IS_ACTIVE",
	"DATE_JOINED",
	"IS_STAFF",
	"ADDRESS",
	"PHONE"
)
VALUES
	(
		1,
		'pbkdf2_sha256$12000$u0ihF631iow2$Gg254Cz5Nu6Ph/uKis0fxG3zDLxPQUp6yq3Z5v4ud6I=',
		TO_TIMESTAMP (
			'2014-03-26 16:39:15:343000',
			'SYYYY-MM-DD HH24:MI:SS:FF6'
		),
		1,
		NULL,
		'admin',
		'Admin',
		'admin@admin.com',
		1,
		TO_TIMESTAMP (
			'2014-03-26 16:39:15:343000',
			'SYYYY-MM-DD HH24:MI:SS:FF6'
		),
		1,
		'address',
		'111'
	);