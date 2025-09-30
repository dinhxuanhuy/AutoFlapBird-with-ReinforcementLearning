# agent.py
import json
import os
import random

class Agent(object):
    """
    Q-learning Agent cho Flappy Bird (dựa trên rl-flappybird).
    - State format: "x0_y0_vel"
      x0: khoảng cách ngang từ bird tới cạnh trái của ống (discretized)
      y0: khoảng cách dọc từ bird tới cạnh trên của lỗ hổng (discretized)
      vel: velocity hiện tại (int)
    - Agent.act(...) trả 0 (no flap) hoặc 1 (flap).
    - Lưu experiences vào self.moves để cập nhật Q khi game kết thúc (update_scores / terminate_game).
    """

    def __init__(self, path="data/qvalues.json", alpha=0.7, gamma=1.0, epsilon=0.0):
        self.path = path
        self.alpha = alpha   # learning rate (lr)
        self.gamma = gamma   # discount factor
        self.epsilon = epsilon  # exploration prob (nếu >0 sẽ epsilon-greedy)
        self.qvalues = {}
        self.gameCNT = 0
        self.r = {0: 0, 1: -1000}  # reward: 0=alive step, 1=penalty at death
        self.lr = self.alpha
        self.discount = self.gamma

        self.last_state = "0_0_0"   # initial state string
        self.last_action = 0
        self.moves = []   # list of (last_state, last_action, new_state)
        self.max_score = 0
        # ensure dir exists
        d = os.path.dirname(self.path)
        if d and not os.path.exists(d):
            os.makedirs(d)

        self.load_qvalues()
        self.initStateIfNull(self.last_state)

    # ---------- Persistence ----------
    def load_qvalues(self):
        """Load q-values từ file json nếu có."""
        self.qvalues = {}
        try:
            with open(self.path, "r") as f:
                self.qvalues = json.load(f)
        except Exception:
            # file không tồn tại hoặc không đọc được -> khởi tạo rỗng
            self.qvalues = {}

    def dump_qvalues(self, force=False):
        """Lưu toàn bộ q-table ra file (force để ép lưu)."""
        if force:
            try:
                with open(self.path, "w") as f:
                    json.dump(self.qvalues, f)
                print(f"Saved Q-table ({len(self.qvalues)} keys) to {self.path}")
            except Exception as e:
                print("Failed saving qvalues:", e)

    def save_qvalues(self):
        """
        Gọi định kỳ để gom trải nghiệm cũ tránh dùng quá nhiều memory.
        (Giữ gần giống logic bản gốc.)
        """
        if len(self.moves) > 6_000_000:
            history = list(reversed(self.moves[:5_000_000]))
            for exp in history:
                state, act, new_state = exp
                # đảm bảo state tồn tại
                self.initStateIfNull(state)
                self.initStateIfNull(new_state)
                self.qvalues[state][act] = (1 - self.lr) * self.qvalues[state][act] + \
                    self.lr * ( self.r[0] + self.discount * max(self.qvalues[new_state][0:2]) )
            # cắt buffer
            self.moves = self.moves[5_000_000:]

    def initStateIfNull(self, state):
        """Nếu state chưa có trong q-table, khởi tạo giá trị mặc định [Q_no_flap, Q_flap, visit_count]"""
        if self.qvalues.get(state) is None:
            self.qvalues[state] = [0.0, 0.0, 0]
            num = len(self.qvalues)
            if num > 20000 and num % 1000 == 0:
                print(f"======== Total state: {num} ========")

    # ---------- Pipe selection helper ----------
    def _select_nearest_pipe(self, x, pipes):
        """
        Chọn pipe sắp tới nhất.
        pipes có thể là:
         - None -> return None
         - 1 Pipe object -> trả nó
         - list of Pipe -> duyệt tìm pipe chưa qua: p.x + p.pipe_width >= bird_x -> return first
        Nếu không tìm thấy -> return None
        """
        if pipes is None:
            return None

        # nếu truyền 1 object pipe
        if hasattr(pipes, "x") and hasattr(pipes, "gapY"):
            return pipes

        # nếu truyền list
        try:
            for p in pipes:
                if not hasattr(p, "x"):
                    continue
                pw = getattr(p, "pipe_width", 0)
                # pipe chưa qua bird nếu cạnh phải ống >= bird.x
                if p.x + pw >= x:
                    return p
        except Exception:
            pass
        return None
    def record_score(self, score):
        """Ghi nhận điểm số cao nhất (nếu cần)."""
        if score > self.max_score:
            self.max_score = score
            print("You reached new max score:", self.max_score)
            if score > 100:
                self.dump_qvalues(force=True)
        elif score == self.max_score and score > 10000:
            self.dump_qvalues(force=True)
    # ---------- State / Action ----------
    def get_state(self, x, y, vel, pipe_or_pipes):
        """
        Sinh state string từ bird (x,y), vel và pipe (nearest).
        Trả "0_0_0" nếu không có pipe.
        """
        pipe = self._select_nearest_pipe(x, pipe_or_pipes)
        if pipe is None:
            state = "0_0_0"
            self.initStateIfNull(state)
            return state

        # Lấy thông tin từ Pipe object: pipe.x và pipe.gapY (gapY = top of gap)
        pipe_x = getattr(pipe, "x", 0)
        gap_top = getattr(pipe, "gapY", None)
        # nếu pipe không có gapY (lỗi), fallback dùng top_rect.y nếu có
        if gap_top is None:
            gap_top = getattr(pipe, "top_rect", None)
            if gap_top is not None and hasattr(gap_top, "y"):
                gap_top = gap_top.y
            else:
                gap_top = 0

        # tính khoảng cách
        x0 = pipe_x - x
        y0 = gap_top - y

        # discretize giống mono code để giảm số state
        if x0 < -40:
            x0 = int(x0)
        elif x0 < 140:
            x0 = int(x0) - (int(x0) % 10)
        else:
            x0 = int(x0) - (int(x0) % 70)

        if -180 < y0 < 180:
            y0 = int(y0) - (int(y0) % 10)
        else:
            y0 = int(y0) - (int(y0) % 60)

        state = f"{int(x0)}_{int(y0)}_{int(vel)}"
        self.initStateIfNull(state)
        return state

    def act(self, x, y, vel, pipe_or_pipes):
        """
        Chọn action (0=no flap, 1=flap) dựa trên state hiện tại.
        Ghi lại experience (last_state, last_action, new_state) vào moves.
        """
        state = self.get_state(x, y, vel, pipe_or_pipes)

        # append experience
        self.moves.append((self.last_state, self.last_action, state)) # thêm vào lịch sử di chuyển
        # mảng move gồm (last_state, last_action, new_state)
        # ví dụ: ("50_20_3", 0, "40_15_2")
        # maintain qvalues size if needed
        self.save_qvalues()

        # ensure current state initialized
        self.initStateIfNull(state)

        # epsilon-greedy optional
        if random.random() < self.epsilon:
            action = random.choice([0, 1])
        else:
            action = 0 if self.qvalues[state][0] >= self.qvalues[state][1] else 1

        self.last_state = state
        self.last_action = action
        return action

    # ---------- Learning updates ----------
    def update_scores(self, died=True, printLogs=False):
        """
        Cập nhật Q-values khi game kết thúc.
        Duyệt history (self.moves) theo thứ tự ngược và cập nhật Q.
        """
        if not self.moves:
            return

        history = list(reversed(self.moves))
        # mảng move gồm (last_state, last_action, new_state)
        # ví dụ: ("50_20_3", 0, "40_15_2")
        # xo yo vel
        # high_death_flag:
        try:
            high_death_flag = True if int(history[0][2].split("_")[1]) > 120 else False
            # nếu y0 (khoảng cách dọc tới lỗ hổng) > 120 thì coi như chết cao
        except Exception:
            high_death_flag = False

        t = 0
        last_flap = True
        for exp in history:
            t += 1
            state, act, new_state = exp
            self.initStateIfNull(state)
            self.initStateIfNull(new_state)

            # increment visit count
            try:
                self.qvalues[state][2] += 1
            except Exception:
                pass

            # choose reward

            if t <= 2: # Hai bước cuối cùng trước khi chết luôn bị phạt nặng:
                cur_reward = self.r[1]
                if act:
                    last_flap = False
            elif (last_flap or high_death_flag) and act: # nếu trước đó flap hoặc chết cao và lần này cũng flap -> phạt
                cur_reward = self.r[1]
                high_death_flag = False
                last_flap = False
            else:
                cur_reward = self.r[0]

            # Q-learning update
            self.qvalues[state][act] = (1 - self.lr) * self.qvalues[state][act] + \
                                       self.lr * (cur_reward + self.discount * max(self.qvalues[new_state][0:2]))

        if printLogs:
            print(f"Game {self.gameCNT}: Updated {len(self.moves)} experiences")
        self.gameCNT += 1
        self.moves = []
        self.last_state = "0_0_0"
        self.last_action = 0

    def terminate_game(self,alive=False):
        """Compatibility: gọi khi muốn cập nhật Q và reset (giống bản gốc)."""
        if alive==True:
            self.update_scores(died=False, printLogs=True)
        self.dump_qvalues(force=True)

    # optional helper
    def max_q(self):
        """Trả Q-value lớn nhất hiện có (dùng để debug)."""
        if not self.qvalues:
            return 0.0
        return max(max(v[0], v[1]) for v in self.qvalues.values())
