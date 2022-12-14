<template>
  <vDialog :show="showDialog" @showEmit="hideDialog">
    <template #header>Добавление оценки</template>
    <form @submit.prevent="mark.add(rememberID)" class="flex flex-col gap-5">
      <div class="flex gap-4">
        <vInput
            placeholder="Введите причину оценки"
            v-model="mark.data.title"
            required
        />
        <vSelect :items="marks" firstItem="Оценка" objectKey="mark" @item="mark.select" required />
      </div>
      <vButton type="submit">Добавить оценку</vButton>
    </form>
  </vDialog>
  <!--  Мы настолько сильно любим проколледж, что решили убрать возможность удалять и изменять оценки.
     Теперь их можно только добавлять! =) -->
  <main class="flex flex-col w-full h-full">
    <header class="flex items-center justify-between p-3 bg-[#4A4A4A] px-50">
      <p
        class="
          text-2xl
          transition-all
          cursor-pointer
          select-none
          text-animated
          hover:opacity-70
          active:opacity-90
        "
        @click="currentWindow = undefined"
      >
        Mark System
      </p>
      <p v-if="userInfo.admin" class="opacity-20 select-none">
        Панель администратора
      </p>
      <div class="flex gap-8 items-center">
        <div v-if="userInfo.name === undefined && currentSubject.title === undefined" class="flex flex-col text-center cursor-default">
          <div class="i-line-md:loading-loop" />
        </div>
        <div v-else class="flex flex-col text-center cursor-default">
          <p class="showDownAnim">{{ userInfo.name }}</p>
          <p class="text-sm opacity-50 showDownAnim">{{ currentSubject.title }}</p>
        </div>
        <i
          class="
            text-3xl
            transition-all
            cursor-pointer
            i-tabler:logout
            hover:opacity-80
            active:opacity-60
          "
          @click="user.logout()"
        />
      </div>
    </header>
    <main class="flex flex-auto gap-5 my-5 px-50">
      <section
        class="
          w-1/6
          h-full
          flex flex-col
          divide-y-2
          gap-10
          bg-[#4A4A4A]
          rounded-md
          opacity-0
          showAnim
        "
      >
        <div v-if="userInfo.admin">
          <div
            class="
              py-2
              my-2
              w-full
              text-center
              bg-white bg-opacity-0
              transition-all
              cursor-pointer
              select-none
              hover:bg-opacity-10
              active:bg-opacity-30
            "
            @click="currentWindow = 'create'"
          >
            Создать
          </div>
        </div>
        <div v-else>
          <div
            class="
              flex flex-col
              gap-3
              py-2
              my-2
              w-full
              text-center
              bg-white bg-opacity-0
              transition-all
              cursor-pointer
              select-none
              hover:bg-opacity-10
              active:bg-opacity-30
            "
            @click="currentWindow = 'markbook'"
          >
            Журнал
          </div>
        </div>
      </section>
      <section
        :class="`flex-auto rounded-md bg-[#4A4A4A] ${
          loading ? 'hideAnim' : 'showAnim'
        }`"
      >
        <!--        for admin-->
        <div
          v-if="currentWindow === 'create' && userInfo.admin === true"
          class="
            grid grid-cols-2 grid-rows-2 grid-flow-col
            gap-5
            p-10
            w-full
            h-full
            opacity-0
            showAnim
          "
        >
          <div
            class="
              flex flex-col
              gap-5
              p-5
              rounded-md
              border border-white border-opacity-30
              shadow-xl
              transition-all
              cursor-default
              select-none
              shadow-black shadow-opacity-5
              hover:-translate-x-1
              hover:-translate-y-1
              hover:shadow-opacity-10
              hover:shadow-2xl
              hover:border-opacity-80
            "
          >
            <p class="text-center">Создание группы</p>
            <vInput
              placeholder="Введите название группы"
              v-model="values.group.name"
            />
            <vButton
              type="success"
              @click="
                admin.create.group(values.group.name);
                clearObjValue(values.group);
              "
              >Создать группу</vButton
            >
            <Transition name="hideShow">
              <p
                class="text-center text-green-400 text-md"
                v-show="states.group !== false"
              >
                Группа успешно создана! ID: {{ ids.group }}
              </p>
            </Transition>
          </div>
          <div
            class="
              flex flex-col
              gap-5
              p-5
              rounded-md
              border border-white border-opacity-30
              shadow-xl
              transition-all
              cursor-default
              select-none
              shadow-black shadow-opacity-5
              hover:-translate-x-1
              hover:-translate-y-1
              hover:shadow-opacity-10
              hover:shadow-2xl
              hover:border-opacity-80
            "
          >
            <p class="text-center">Создание студента</p>
            <vInput
              placeholder="Введите ФИО студента"
              v-model="values.student.name"
            />
            <vInput
              placeholder="Введите id группы"
              v-model="values.student.group_id"
            />
            <vButton
              type="success"
              @click="
                admin.create.student(
                  values.student.name,
                  values.student.group_id
                );
                clearObjValue(values.student);
              "
              >Создать студента</vButton
            >
            <Transition name="hideShow">
              <p
                class="text-center text-green-400 text-md"
                v-show="states.student !== false"
              >
                Студент успешно создан! ID: {{ ids.student }}
              </p>
            </Transition>
          </div>
          <div
            class="
              flex flex-col
              gap-5
              p-5
              rounded-md
              border border-white border-opacity-30
              shadow-xl
              transition-all
              cursor-default
              select-none
              shadow-black shadow-opacity-5
              hover:-translate-x-1
              hover:-translate-y-1
              hover:shadow-opacity-10
              hover:shadow-2xl
              hover:border-opacity-80
            "
          >
            <p class="text-center">Создание предмета</p>
            <vInput
              placeholder="Введите название предмета"
              v-model="values.subject.title"
            />
            <vInput
              placeholder="Введите id преподавателя"
              v-model="values.subject.tid"
            />
            <vInput
              placeholder="Введите список ID групп"
              v-model="values.subject.groups"
            />
            <vButton
              type="success"
              @click="
                admin.create.subject(
                  values.subject.title,
                  values.subject.tid,
                  values.subject.groups
                );
                clearObjValue(values.subject);
              "
              >Создать</vButton
            >
            <Transition name="hideShow">
              <p
                class="text-center text-green-400 text-md"
                v-show="states.subject !== false"
              >
                Предмет успешно создан! ID: {{ ids.subject }}
              </p>
            </Transition>
          </div>
          <div
            class="
              flex flex-col
              gap-5
              p-5
              rounded-md
              border border-white border-opacity-30
              shadow-xl
              transition-all
              cursor-default
              select-none
              shadow-black shadow-opacity-5
              hover:-translate-x-1
              hover:-translate-y-1
              hover:shadow-opacity-10
              hover:shadow-2xl
              hover:border-opacity-80
            "
          >
            <p class="text-center">Создание преподавателя</p>
            <vInput
              placeholder="Введите имя преподавателя"
              v-model="values.teacher.name"
            />
            <vInput
              placeholder="Введите почту "
              v-model="values.teacher.email"
            />
            <vInput
              placeholder="Введите пароль"
              v-model="values.teacher.password"
            />
            <vButton
              type="success"
              @click="
                admin.create.teacher(
                  values.teacher.name,
                  values.teacher.email,
                  values.teacher.password
                );
                clearObjValue(values.teacher);
              "
              >Создать</vButton
            >
            <Transition name="hideShow">
              <p
                class="text-center text-green-400 text-md"
                v-show="states.teacher !== false"
              >
                Преподаватель успешно создан! ID: {{ ids.teacher }}
              </p>
            </Transition>
          </div>
        </div>
        <!-- for teachers-->
        <div
          v-else-if="currentWindow === 'markbook' && userInfo.admin === false"
          class="flex flex-col gap-10 w-full h-full showAnim"
        >
          <div class="flex gap-10 justify-center my-2 w-full">
            <div>
              <vSelect :items="groups" objectKey="name" firstItem="Выберите группу" @item="select.group" />
            </div>
          </div>
          <div class="flex flex-auto justify-center items-center">
            <div
              v-if="select.selected.name !== undefined"
              class="flex justify-center"
            >
              <table class="cursor-default min-w-4/5 text-xl">
                <tr>
                  <th>Ученик</th>
                  <th>Оценки</th>
                </tr>
                <tr
                  v-for="(value, name) in currentGroup"
                  :key="name"
                  class="hover:bg-white hover:bg-opacity-5"
                >
                  <th v-if="students[name] !== undefined" class="showDownAnim">{{ students[name] }}</th>
                  <th v-else class="h-full w-full flex items-center justify-center"><div class="i-line-md:loading-loop" /></th>
                  <th>
                    <div class="flex gap-3 items-center">
                      <div v-for="mark in value" :key="mark.id">
                        <div
                          v-if="mark.score === 5"
                          class="hint--top"
                          :aria-label="`${mark.title}, ${formatDistance(
                            fromUnixTime(mark.timestamp),
                            new Date(),
                            {
                              locale: ru,
                            }
                          )} назад`"
                        >
                          <p class="text-green-400">5</p>
                        </div>
                        <div
                          v-if="mark.score === 4"
                          class="hint--top"
                          :aria-label="`${mark.title}, ${formatDistance(
                            fromUnixTime(mark.timestamp),
                            new Date(),
                            {
                              locale: ru,
                            }
                          )} назад`"
                        >
                          <p class="text-green-600">4</p>
                        </div>
                        <div
                          v-if="mark.score === 3"
                          class="hint--top"
                          :aria-label="`${mark.title}, ${formatDistance(
                            fromUnixTime(mark.timestamp),
                            new Date(),
                            {
                              locale: ru,
                            }
                          )} назад`"
                        >
                          <p class="text-orange-500">3</p>
                        </div>
                        <div
                          v-if="mark.score === 2"
                          class="hint--top"
                          :aria-label="`${mark.title}, ${formatDistance(
                            fromUnixTime(mark.timestamp),
                            new Date(),
                            {
                              locale: ru,
                            }
                          )} назад`"
                        >
                          <p class="text-red-500">2</p>
                        </div>
                      </div>
                      <!-- TODO: add here mark btn -->
                      <div class="i-tabler:square-plus opacity-30 cursor-pointer hover:opacity-100 transition-all" @click="rememberID = name; showDialog = true"></div>
                    </div>
                  </th>
                </tr>
              </table>
            </div>
            <div v-else-if="currentGroup === undefined">
              В группе отсутствуют ученики.
            </div>
            <div v-else>Выберите группу</div>
          </div>
        </div>
        <!-- not selected window -->
        <div
          v-else-if="currentWindow === undefined"
          class="
            flex
            justify-center
            items-center
            w-full
            h-full
            text-2xl
            showAnim
          "
        >
          Выберите секцию
        </div>
        <div v-else>ты как тут оказался ваще ыыыыыыыыыы</div>
      </section>
    </main>
  </main>
</template>

<script setup>
// import libs
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import router from "../../router/index.js";
import axios from "axios";
import { formatDistance, fromUnixTime } from "date-fns";
import { ca, ru } from "date-fns/locale";

// import components
import vButton from "../../components/v-button.vue";
import vInput from "../../components/v-input.vue";
import vDialog from "../../components/v-dialog.vue";
import vSelect from "../../components/v-select.vue";
import getSeconds from "date-fns/fp/getSeconds/index.js";


const userInfo = ref({
  token: undefined,
  id: undefined,
  admin: undefined,
  admin_token: undefined,
  name: undefined,
});

const currentWindow = ref(undefined);
const showDialog = ref(false)
const loading = ref(false);
const groups = ref([]);
const currentSubject = ref({});
const currentGroup = ref();
const students = ref([]);

function hideDialog(value) {
  showDialog.value = value
}

function getStudentName(sid) {
  axios.get(`http://127.0.0.1:8000/student/id${sid}`).then((res) => {
    students.value[sid] = res.data.response.name;
  });
}

const select = ref({
  group: (value) => {
    loading.value = true;
    rememberSelect.value = value;
    select.value.selected = groups.value.find((group) => group.name === value);
    console.log(groups.value.find((group) => group.name === value))
    axios
      .get(
        `http://127.0.0.1:8000/subject/marks${currentSubject.value.s_id}:${select.value.selected.group_id}`
      )
      .then((res) => {
        currentGroup.value = res.data.response;
        students.value = [];
        for (const [key] of Object.entries(currentGroup.value)) {
          getStudentName(key);
        };
        loading.value = false;
      });
  },
  selected: {
    name: undefined,
    group_id: undefined,
  },
});

function clearObjValue(obj) {
  for (const [key] of Object.entries(obj)) {
    obj[key] = "";
  }
}

const rememberSelect = ref();
const rememberID = ref();
const rememberLastTitle = ref("");

const marks = ref([
  {"mark": 5},
  {"mark": 4},
  {"mark": 3},
  {"mark": 2},
])

const mark = ref({
  select: (score) => {
    mark.value.data.score = score
  },
  data: {
    title: "",
    score: 2,
  },
  update: () => {
    select.value.group(rememberSelect.value); // here we get all marks, re-render window
    showDialog.value = false;
    mark.value.data.title = rememberLastTitle.value; // remember title and load it to modal
  },
  add: (student_id) => {
    rememberLastTitle.value = mark.value.data.title;
    axios.post(`http://127.0.0.1:8000/mark/?student_id=${student_id}&subject_id=${currentSubject.value.s_id}&title=${mark.value.data.title}&score=${mark.value.data.score}&access_token=${userInfo.value.token}`)
        .then((res) => {console.log(res.data)})
        .catch((err) => {throw err;});
    mark.value.update();
  },
  remove: (student_id) => {
    rememberLastTitle.value = mark.value.data.title;
    axios.post(`http://127.0.0.1:8000/mark/?student_id=${student_id}&subject_id=${currentSubject.value.s_id}&title=${mark.value.data.title}&score=${mark.value.data.score}&access_token=${userInfo.value.token}`)
        .then((res) => {console.log(res.data)})
        .catch((err) => {throw err;});
    mark.value.update();
  }
})

const user = ref({
  logout: () => {
    Cookies.remove("userInfo");
    Cookies.remove("admin");
    router.push("/auth");
  },
});

const admin = {
  get: {
    /**
     * Получение списка всех групп
     */
    allGroups: () => {
      axios
        .get("http://127.0.0.1:8000/group/all")
        .then((res) => {
          return res.data.response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    /**
     * Получение оценки по ID
     * @param {Number} mid mark id
     */
    markByID: (mid) => {
      axios
        .get(`http://127.0.0.1:8080/mark/id${mid}`)
        .then((res) => {
          return res.data.response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    /**
     * Получение группы по ID
     * @param {Number} gid group id
     */
    groupByID: (gid) => {
      axios
        .get(`http://127.0.0.1:8080/student/group${gid}`)
        .then((res) => {
          return res.data.response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    /**
     * Получение предмета по ID
     * @param {Number} sid subject id
     */
    subjectByID: async (sid) => {
      const res = await axios.get(`http://127.0.0.1:8080/subject/id${sid}`);
      return res.data;
    },
    /**
     * Получение всех оценок по предмету и группе
     * @param {Number} sid subject id
     * @param {Number} gid group id
     */
    marks: (sid, gid) => {
      axios
        .get(`http://127.0.0.1:8080/student/group${gid}`)
        .then((res) => {
          return res.data.response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    /**
     * Получение аккаунта преподавателя
     * @param {Number} tid ID преподавателя
     */
    teacherByID: (tid) => {
      axios
        .get(`https://127.0.0.1:8080/teacher/id${sid}`)
        .then(() => {
          return res.data.response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  create: {
    /**
     * Создание группы
     * @param {String} name Имя группы
     */
    group: (name) => {
      axios
        .post(`http://127.0.0.1:8000/group/?name=${name}`, {
          admin_token: userInfo.value.admin_token,
        })
        .then((res) => {
          states.value.group = true;
          ids.value.group = res.data.response;
          setTimeout(() => {
            states.value.group = false;
          }, 5000);
        })
        .catch((res) => {
          console.log(res);
        });
    },
    /**
     * Создание предмета
     * @param {String} title Название предмета
     * @param {Number} tid ID преподавателя
     * @param {String} groups Список групп, через запятую
     */
    subject: (title, tid, groups) => {
      axios
        .post(
          `http://127.0.0.1:8000/subject/?title=${title}&teacher_id=${tid}&groups=${groups}`,
          {
            admin_token: userInfo.value.admin_token,
          }
        )
        .then((res) => {
          states.value.subject = true;
          ids.value.subject = res.data.response;
          setTimeout(() => {
            states.value.subject = false;
          }, 5000);
        })
        .catch((res) => {
          console.log(res);
        });
    },
    /**
     * Создание студента
     * @param {String} name Имя студента
     * @param {Number} group_id ID группы
     */
    student: (name, group_id) => {
      axios
        .post(
          `http://127.0.0.1:8000/student/?name=${name}&group_id=${group_id}`,
          {
            admin_token: userInfo.value.admin_token,
          }
        )
        .then((res) => {
          states.value.student = true;
          ids.value.student = res.data.response;
          setTimeout(() => {
            states.value.student = false;
          }, 5000);
        })
        .catch((res) => {
          console.log(res);
        });
    },
    /**
     * Создание преподавателя
     * @param {String} name Имя преподавателя
     * @param {String} email Почта преподавателя
     * @param {String} password Пароль преподавателя
     */
    teacher: (name, email, password) => {
      axios
        .post(
          `http://127.0.0.1:8000/teacher/?name=${name}&email=${email}&password=${password}`,
          {
            admin_token: userInfo.value.admin_token,
          }
        )
        .then((res) => {
          states.value.teacher = true;
          ids.value.teacher = res.data.response;
          setTimeout(() => {
            states.value.teacher = false;
          }, 5000);
        })
        .catch((res) => {
          console.log(res);
        });
    },
  },
};

const states = ref({
  group: false,
  subject: false,
  student: false,
  teacher: false,
});

const ids = ref({
  group: "",
  subject: "",
  student: "",
  teacher: "",
});

const values = ref({
  group: {
    name: "",
  },
  subject: {
    title: "",
    tid: "",
    groups: "",
  },
  student: {
    name: "",
    group_id: "",
  },
  teacher: {
    name: "",
    email: "",
    password: "",
  },
});

onMounted(async () => {
  const nigger = async () => {
    return await axios
      .get(
        `http://127.0.0.1:8000/teacher/id${
          JSON.parse(Cookies.get("userInfo")).id
        }`
      )
      .then((res) => {
        return res.data.response;
      })
      .catch((err) => {
        console.log(err.response);
      });
  };

  if (Cookies.get("userInfo") !== undefined) {
    userInfo.value = {
      token: JSON.parse(Cookies.get("userInfo")).access_token,
      id: JSON.parse(Cookies.get("userInfo")).id,
      admin: JSON.parse(Cookies.get("userInfo")).admin,
      admin_token: JSON.parse(Cookies.get("userInfo")).admin
        ? "marksystem:v1:hui"
        : undefined,
      name: await nigger().then((res) => {
        return res.name;
      }),
      email: await nigger().then((res) => {
        return res.email;
      }),
    };

    if (userInfo.value.admin === false) {
      axios
        .get("http://127.0.0.1:8000/subject/all")
        .then((res) => {
          currentSubject.value = res.data.response.items.find(
            (subject) => subject.teacher_id === userInfo.value.id
          );
          currentSubject.value.groups.forEach((value) => {
            axios
              .get("http://127.0.0.1:8000/group/all")
              .then((res) => {
                groups.value.push(
                  res.data.response.items.find(
                    (group) => group.group_id === value
                  )
                );
              })
              .catch((err) => {
                console.error(err);
              });
          });
        })
        .catch((err) => {
          console.error(err);
        });
    }
  } else {
    router.push("/auth?err=Войдите в аккаунт.");
  }
});
</script>

<style>
table,
th,
td {
  font-weight: normal;
  border: white 1px solid;
}

th {
  padding: 10px;
}
</style>
