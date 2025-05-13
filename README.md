# BaiTapCaNhan
8-Puzzle: Trò chơi giải đố trên bảng 3x3 với 8 ô số (1-8) và 1 ô trống. Sử dụng những thuật toán tìm kiếm bằng AI để tìm ra giải pháp cho bài toán 1 cách thật hiệu quả và tối ưu nhất.
=======
Giới thiệu bài toán 8_puzzle
8-Puzzle Solver là một đồ án phần mềm giải bài toán 8-Puzzle (trò chơi xếp ô số 3x3) được phát triển bằng Python, sử dụng Pygame cho giao diện người dùng và Plotly để trực quan hóa hiệu suất. Chương trình tích hợp nhiều thuật toán tìm kiếm để giải bài toán và so sánh hiệu suất.

1. Mục tiêu
Mục tiêu cốt lõi của dự án là xây dựng một chương trình toàn diện và linh hoạt để giải quyết bài toán 8-puzzle – một bài toán kinh điển và nền tảng trong lĩnh vực trí tuệ nhân tạo cũng như khoa học máy tính – thông qua việc tích hợp nhiều thuật toán đa dạng và tiên tiến, từ các phương pháp tìm kiếm truyền thống đến các kỹ thuật học tăng cường hiện đại. Dự án không chỉ dừng lại ở việc tạo ra một công cụ đơn thuần để tìm lời giải cho bài toán, mà còn đặt trọng tâm vào việc thiết kế một nền tảng mạnh mẽ, hỗ trợ nghiên cứu chuyên sâu, học tập thực tiễn, và khám phá các cách tiếp cận khác nhau trong việc giải quyết các vấn đề phức tạp của trí tuệ nhân tạo, từ đó mang lại giá trị giáo dục và thực tiễn cho người dùng.

2.Nội Dung

2.1 Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search Algorithms)
Các yếu tố chính trong mô hình bài toán và phương pháp giải
+	Trạng thái khởi đầu
Bắt đầu từ một bảng 3x3 gồm 8 ô số và một ô trống (0), ví dụ: [[1, 2, 3], [0, 5, 6], [4, 7, 8]].
+	Trạng thái cần đạt tới
Đích đến là cấu hình chuẩn của bài toán, với các số được sắp xếp theo thứ tự tăng dần từ trái sang phải, từ trên xuống dưới và ô trống nằm ở vị trí cuối cùng: [[1, 2, 3], [4, 5, 6], [7, 8, 0]].
+	Không gian trạng thái
Bao gồm toàn bộ các cách sắp xếp hợp lệ của 8 số và ô trống trong lưới 3x3 – tức là tập hợp tất cả các cấu hình có thể xuất hiện trong quá trình giải.
+	Tập hành động có thể thực hiện
Tại mỗi bước, ô trống có thể di chuyển lên, xuống, sang trái hoặc phải, nhằm hoán đổi vị trí với ô số kề cận.
+	Chi phí hành động
Mỗi hành động được tính một chi phí bằng 1, với mục tiêu tìm con đường ngắn nhất từ trạng thái đầu đến trạng thái cuối.
+	Chiến lược giải quyết
Chuỗi các trạng thái tạo thành lời giải được xây dựng thông qua việc áp dụng các thuật toán tìm kiếm không sử dụng thông tin hướng dẫn: BFS, DFS, UCS và IDS.
![2 1](https://github.com/user-attachments/assets/a31309ec-b9f4-4cee-a5d9-256778be0448)


________________________________________
Đánh giá các thuật toán
+	BFS (Tìm kiếm theo chiều rộng):
Duyệt lần lượt tất cả các trạng thái theo từng lớp. Dễ bị tốn bộ nhớ vì cần lưu nhiều trạng thái cùng lúc, nhất là khi không gian trạng thái lớn.
+	DFS (Tìm kiếm theo chiều sâu):
Tiết kiệm bộ nhớ hơn do chỉ lưu một nhánh tại một thời điểm. Tuy nhiên, dễ bị lạc hướng nếu mục tiêu nằm gần gốc mà DFS lại ưu tiên đi sâu trước.
+	UCS (Tìm kiếm chi phí đồng đều):
Gần giống BFS nhưng ưu tiên đường đi có tổng chi phí thấp hơn. Trong 8-Puzzle, do chi phí các bước là như nhau, UCS hoạt động tương tự BFS.
+	IDS (Tìm kiếm sâu dần lặp lại):
Kết hợp hiệu quả của DFS và BFS bằng cách thực hiện tìm kiếm theo từng độ sâu và lặp lại nhiều lần. Không tốn quá nhiều bộ nhớ, phù hợp với bài toán này.
________________________________________
Tổng kết
+	IDS nổi bật vì dung hòa được giữa bộ nhớ và hiệu quả giải, thường cho kết quả tốt trong các bài toán như 8-Puzzle.
+	DFS dễ bị rơi vào các nhánh không có lời giải, dẫn đến kém hiệu quả, đặc biệt nếu lời giải nằm ở độ sâu thấp.

2.2 Nhóm thuật toán tìm kiếm có thông tin (Informed Search Algorithms)

Cấu trúc bài toán và hướng tiếp cận
  +Trạng thái khởi đầu
  Bài toán bắt đầu với một lưới 3x3, chứa các số từ 1 đến 8 và một ô trống (ký hiệu là 0). Ví dụ trạng thái đầu vào: [[2, 0, 3], [1, 4, 6], [7, 5, 8]].
  
  +Trạng thái mục tiêu
  Mục tiêu là đưa lưới về cấu hình chuẩn: [[1, 2, 3], [4, 5, 6], [7, 8, 0]], nơi các số được sắp xếp tăng dần và ô trống ở góc dưới bên phải.
  
  +Không gian trạng thái
  Bao gồm tất cả các cách sắp xếp hợp lệ của các ô số trong bảng 3x3, hình thành khi người giải thực hiện các hành động di chuyển ô trống.
  
  +Hành động khả thi
  Tại mỗi bước, ô trống có thể dịch chuyển lên trên, xuống dưới, sang trái hoặc sang phải để đổi chỗ với ô liền kề – miễn là hành động hợp lệ trong giới hạn lưới.
  
  +Chi phí hành động
  Mỗi lần di chuyển được gán chi phí bằng 1. Do đó, mục tiêu của bài toán là tìm đường đi ngắn nhất để tối ưu tổng chi phí.
  
  +Chiến lược giải quyết
  Dựa trên các thuật toán có sử dụng thông tin định hướng (heuristic), bao gồm: Greedy Best-First Search (GBFS), A* và Iterative Deepening A* (IDA*).
  
  ![2 2](https://github.com/user-attachments/assets/e879afdd-635a-4f66-9894-3b9777d23438)

Phân tích thuật toán
  +GBFS (Tìm kiếm tham lam theo giá trị heuristic):
  Tập trung tìm kiếm dựa trên giá trị heuristic hiện tại, bỏ qua chi phí tích lũy. Nhờ đó, GBFS hoạt động rất nhanh và duyệt ít trạng thái. Tuy nhiên, nó dễ bị kẹt ở điểm tối ưu cục bộ nếu hàm heuristic không chính xác, dẫn đến không đảm bảo tìm được đường đi tốt nhất.
  
  +A* (Tìm kiếm theo tổng chi phí và heuristic):
  Kết hợp giữa chi phí đã đi (g(n)) và giá trị ước lượng đến đích (h(n)) để đưa ra quyết định tại mỗi bước, theo công thức f(n) = g(n) + h(n). A* thường cho kết quả chính xác và tối ưu, nhưng sử dụng nhiều bộ nhớ hơn do phải lưu trữ hàng đợi ưu tiên lớn.
  
  +IDA* (Tìm kiếm sâu dần sử dụng heuristic):
  Là phiên bản tiết kiệm bộ nhớ của A*, thực hiện tìm kiếm theo từng mức độ giới hạn và lặp lại nhiều lần với giới hạn tăng dần. IDA* có tốc độ cao và tiết kiệm bộ nhớ nhưng có thể duyệt lại nhiều trạng thái nếu heuristic chưa tối ưu.
  
Kết luận
  +IDA* nổi bật nhờ sự cân bằng giữa hiệu suất và tiêu tốn bộ nhớ. Tuy nhiên, để nâng cao hiệu quả, cần cải thiện hàm heuristic nhằm giảm số lượt lặp lại.
  
  +GBFS là lựa chọn phù hợp nếu mục tiêu là tìm giải pháp nhanh, mặc dù không đảm bảo tối ưu toàn cục.
  
  +A* là phương án an toàn nhất khi cần giải pháp chính xác và tối ưu, dù tiêu tốn tài nguyên hơn.

2.3 Nhóm thuật toán tìm kiếm cục bộ (Local Optimization Algorithms)
Thành phần bài toán và phương pháp giải quyết
+	Trạng thái ban đầu
Xuất phát từ một bảng 3x3 chứa các số từ 1 đến 8 và một ô trống (0), ví dụ: [[1, 3, 6], [4, 2, 0], [7, 5, 8]].
+	Trạng thái đích
Mục tiêu là đưa bảng về cấu hình lý tưởng [[1, 2, 3], [4, 5, 6], [7, 8, 0]], nơi các số được sắp xếp theo thứ tự tăng dần và ô trống nằm ở vị trí cuối cùng.
+	Không gian trạng thái
Gồm toàn bộ các cấu hình hợp lệ của lưới 3x3, được hình thành qua việc di chuyển ô trống đến các vị trí khác nhau để hoán đổi với ô liền kề.
+	Tập hành động
Tại mỗi trạng thái, ô trống có thể di chuyển theo 4 hướng (trái, phải, lên, xuống) nếu không vượt ra ngoài giới hạn bảng.
+	Chi phí hành động
Mỗi thao tác di chuyển được tính là 1 đơn vị chi phí. Do đó, lời giải tốt nhất là lời giải ngắn nhất về số bước.
+	Cách tiếp cận giải bài toán
Các thuật toán trong nhóm này sử dụng chiến lược tối ưu cục bộ để dần tiến tới trạng thái mục tiêu, bao gồm:
Simple Hill Climbing (SHC), Steepest Ascent Hill Climbing (SAHC), Simulated Annealing (SA), Beam Search (BS) và Genetic Algorithm (GA).

__________________________________![2 3](https://github.com/user-attachments/assets/c43396af-1e92-45a0-99e0-cf2667771d20)
______
Đánh giá các thuật toán
+	SHC (Leo đồi đơn giản):
Ưu tiên trạng thái lân cận đầu tiên tốt hơn trạng thái hiện tại và dừng ngay khi không còn cải thiện. Do không kiểm tra toàn bộ lân cận và không có cơ chế thoát cực trị, SHC chạy nhanh nhưng dễ bị mắc kẹt.
+	SAHC (Leo đồi theo độ dốc lớn nhất):
Thay vì chọn ngẫu nhiên, SAHC duyệt toàn bộ trạng thái lân cận để chọn bước tốt nhất. Điều này giúp tránh kẹt ở điểm yếu hơn SHC, nhưng thời gian xử lý mỗi bước dài hơn.
+	SA (Làm nguội mô phỏng):
Áp dụng chiến lược chấp nhận trạng thái xấu hơn trong một số tình huống với xác suất giảm dần theo thời gian (làm nguội). Điều này giúp SA có thể thoát khỏi cực trị cục bộ hiệu quả hơn hai phương pháp leo đồi.
+	BS (Tìm kiếm chùm):
Giới hạn số lượng trạng thái được mở rộng tại mỗi bước (ví dụ: 5 trạng thái tốt nhất), giúp tăng tốc tìm kiếm. Tuy nhiên, nếu chọn beam width quá nhỏ, BS có thể bỏ lỡ lời giải tốt.
+	GA (Thuật toán di truyền):
Lấy cảm hứng từ tiến hóa sinh học, GA hoạt động dựa trên các quần thể trạng thái, chọn lọc và tái tổ hợp để tìm lời giải. Tuy hoạt động tốt trong việc bao phủ không gian rộng, nhưng tốc độ chậm và tiêu tốn nhiều tài nguyên.
+ Random Hill Climbing (RHC): Thời gian chạy trung bình trong nhóm Hill Climbing, vì chỉ chọn ngẫu nhiên một trạng thái lân cận tốt hơn thay vì duyệt hết như SAHC.
________________________________________
Kết luận
+	GA phù hợp với các bài toán cần khai phá toàn diện không gian tìm kiếm và tìm lời giải tối ưu, dù chi phí về thời gian và bộ nhớ cao.
+	SA là một lựa chọn cân bằng tốt giữa hiệu suất và khả năng tránh cực trị cục bộ.
+	BS cho kết quả nhanh hơn GA và SA, tuy nhiên cần lựa chọn tham số cẩn thận để không bỏ lỡ lời giải.
+	Các thuật toán Hill Climbing (SHC, SAHC) hoạt động nhanh và ít tốn tài nguyên, nhưng dễ bị mắc kẹt ở cực trị cục bộ, đặc biệt là SHC.
	
2.4 Nhóm thuật toán tìm kiếm trong môi trường phức tạp (Search in Complex Environments)
 	
Mô hình bài toán và phương pháp tiếp cận
+	Trạng thái khởi đầu
  +	Với AND-OR Search: Xuất phát từ một bảng cụ thể 3x3 gồm các số từ 1 đến 8 và một ô trống (0), ví dụ: [[1, 2, 3], [4, 5, 6], [7, 0, 8]].
  +	Với Belief State Search: Khởi tạo bằng một tập hợp belief states gồm trạng thái gốc và hai trạng thái kề cạnh, phản ánh các khả năng chuyển đổi trong môi trường không quan sát được.
  +	Với Partial Observable Search (POS): Bắt đầu từ tập các belief states có điểm chung là số 1 nằm tại vị trí (0,0) – được hình thành nhờ khả năng quan sát một phần trạng thái ban đầu và trạng thái lân cận.
+	Trạng thái mục tiêu
Mục tiêu là đưa bảng về dạng chuẩn [[1, 2, 3], [4, 5, 6], [7, 8, 0]], với các số xếp theo thứ tự tăng dần và ô trống nằm ở vị trí cuối cùng.
+	Không gian trạng thái
Bao gồm cả các trạng thái xác định (fully observable) và các trạng thái không xác định (uncertain), hình thành từ quá trình di chuyển ô trống và các yếu tố không chắc chắn do thiếu quan sát.
+	Tập hành động
Tại mỗi bước, ô trống có thể di chuyển theo bốn hướng. Tuy nhiên, với các thuật toán trong nhóm này, một hành động có thể dẫn đến nhiều trạng thái tiếp theo – mô phỏng các hệ thống không chắc chắn hoặc không quan sát toàn phần.
+	Chi phí di chuyển
Mỗi bước dịch chuyển được tính chi phí là 1. Mục tiêu của các thuật toán vẫn là tìm đường đi ngắn nhất đến đích, dù trong điều kiện thông tin không đầy đủ.
+	Chiến lược giải quyết
Các thuật toán như AND-OR Search, Belief State Search, và Partial Observable Search (POS) được sử dụng để xử lý các tình huống phức tạp này. Tất cả đều dựa vào việc duy trì và xử lý các tập belief states nhằm tìm ra chuỗi hành động dẫn đến mục tiêu cho toàn bộ các trạng thái có thể xảy ra.
![2 4](https://github.com/user-attachments/assets/1d788062-487f-4adf-b64d-1759759045cd)

________________________________________
Phân tích thuật toán
+	AND-OR Search
Áp dụng cho môi trường không xác định, thuật toán duy trì toàn bộ nhánh AND mà không thu hẹp không gian tìm kiếm, khiến số lượng trạng thái phát sinh rất lớn. Tuy nhiên, thời gian xử lý mỗi trạng thái thấp do không dùng heuristic và chỉ kiểm tra điều kiện đạt mục tiêu hoặc thực hiện hoán đổi đơn giản.
+	Belief State Search
Hoạt động trong môi trường không có khả năng quan sát trực tiếp. Thuật toán cố gắng giảm bớt độ không chắc chắn bằng cách giữ lại 3 trạng thái tốt nhất (dựa trên heuristic). Dù tiết kiệm không gian hơn AND-OR, nhưng việc gọi heuristic nhiều lần làm tăng chi phí tính toán.
+	POS (Partial Observable Search)
Áp dụng khi có thể quan sát được một phần thông tin trạng thái. POS cũng giữ lại các trạng thái belief tốt nhất, nhưng đồng thời tận dụng dữ liệu quan sát để loại bỏ những trạng thái không hợp lệ sớm, từ đó thu nhỏ không gian tìm kiếm. Thời gian xử lý trung bình và số bước đi thường tối ưu hơn nhờ định hướng rõ ràng.
________________________________________
Kết luận
+	POS là lựa chọn hợp lý nhất nếu muốn cân bằng giữa hiệu suất xử lý và quy mô không gian trạng thái, nhờ khả năng quan sát một phần giúp loại trừ sớm các khả năng sai lệch.
+	Belief State Search hiệu quả trong bối cảnh không có quan sát, nhưng chi phí tính toán cao hơn và không gian trạng thái lớn hơn POS.
+	AND-OR Search có tốc độ xử lý nhanh nhưng lại phát sinh nhiều nhánh không cần thiết, thích hợp hơn khi trạng thái ban đầu đã gần sát mục tiêu và không yêu cầu thu hẹp không gian tìm kiếm.

2.5 Nhóm thuật toán tìm kiếm thỏa ràng buộc (Constraint Satisfaction Problem – CSP)
Mô hình bài toán và phương pháp tiếp cận
+	Trạng thái ban đầu
Bắt đầu với một bảng 3x3 hoàn toàn trống ([[None, None, None], [None, None, None], [None, None, None]]). Nhiệm vụ của hệ thống là gán dần các giá trị từ 0 đến 8 vào các ô sao cho toàn bộ các điều kiện ràng buộc đều được đáp ứng.
+	Trạng thái mục tiêu
Cấu hình lý tưởng là [[1, 2, 3], [4, 5, 6], [7, 8, 0]], đại diện cho đích đến hợp lệ theo quy tắc sắp xếp của bài toán 8-Puzzle.
+	Không gian trạng thái
Bao gồm tất cả các khả năng gán giá trị cho lưới 3x3, nhưng bị giới hạn bởi các ràng buộc sau:
  +	Ô tại vị trí (0,0) bắt buộc phải là số 1.
  +	Mỗi số từ 0 đến 8 chỉ xuất hiện đúng một lần trên toàn bảng.
  +	Ràng buộc theo hàng: ô bên phải phải có giá trị lớn hơn ô bên trái đúng 1 đơn vị (trừ ô trống).
  +	Ràng buộc theo cột: ô phía dưới phải lớn hơn ô phía trên đúng 3 đơn vị (trừ ô trống).
  +	Cấu hình cuối cùng phải là trạng thái có thể giải được (tức số nghịch đảo là chẵn).
+	Hành động thực hiện
Hệ thống gán từng giá trị vào ô, sử dụng:
  +	Backtracking Search: duyệt tuần tự, quay lui nếu gặp xung đột.
  +	Forward Checking: mỗi lần gán sẽ đồng thời loại bỏ các giá trị không hợp lệ khỏi domain của các ô khác, giúp tăng hiệu quả và tránh xung đột sớm.
+	Chi phí
Bài toán này không đặt nặng tối ưu hóa số bước mà chủ yếu tập trung vào việc tìm ra một cấu hình hợp lệ duy nhất thỏa tất cả điều kiện đặt ra.
+	Giải pháp đầu ra
Là một chuỗi các bước gán giá trị hợp lệ từ trạng thái rỗng cho đến khi đạt được trạng thái mục tiêu. Các thuật toán như Backtracking và Forward Checking đảm bảo việc tìm kiếm dừng lại khi tất cả ràng buộc đều được thỏa mãn.

______![2 5](https://github.com/user-attachments/assets/fa7126bd-a803-4f88-b59b-67e6555d97f0)
__________________________________
Đánh giá thuật toán
+	Backtracking Search
Tìm kiếm theo chiều sâu, kiểm tra từng bước và quay lui khi có xung đột. Mặc dù đơn giản và dễ cài đặt, nhưng thuật toán này có thể duyệt rất nhiều trạng thái không cần thiết khi không gian tìm kiếm lớn.
+	Forward Checking Search
+	Min-Conflicts Search: Thuật toán bắt đầu từ trạng thái rỗng, gán giá trị và điều chỉnh để giảm xung đột, sử dụng Simulated Annealing để tránh cực trị địa phương. Số trạng thái khám phá thấp nhất nhờ chiến lược sửa lỗi từng bước, nhưng chi phí mỗi bước cao do tính toán xung đột.
Tối ưu hơn Backtracking bằng cách loại bỏ sớm các khả năng không hợp lệ nhờ kỹ thuật kiểm tra forward. Kết hợp với các chiến lược như:
  +	MRV (Minimum Remaining Values): chọn ô có ít giá trị hợp lệ nhất để gán trước.
 +	LCV (Least Constraining Value): ưu tiên gán giá trị ít ảnh hưởng đến ô khác nhất.

Nhờ vậy, số trạng thái duyệt thường thấp hơn, nhưng chi phí tính toán mỗi bước lại cao hơn vì cần duy trì và cập nhật các domain.
________________________________________
Kết luận
+	Backtracking phù hợp cho những bài toán nhỏ hoặc khi cấu trúc ràng buộc đơn giản. Tuy nhiên, khi không gian tìm kiếm mở rộng, nó dễ bị chậm do số trạng thái cần duyệt quá lớn.
+	Forward Checking giúp giảm đáng kể số lượng trạng thái duyệt nhưng đòi hỏi nhiều tính toán hơn tại mỗi bước gán. Đây là lựa chọn hiệu quả khi cần giảm thiểu không gian tìm kiếm, đặc biệt trong các bài toán có nhiều ràng buộc chặt chẽ.
+	Min-Conflicts Search là lựa chọn tốt nhất trong nhóm về không gian trạng thái, với thời gian chạy hợp lý. Nó hiệu quả khi trạng thái ban đầu gần mục tiêu, nhờ khả năng sửa lỗi từng bước.
2.6 Các thành phần cốt lõi trong bài toán và cách tiếp cận giải bằng Q-Learning
+	Trạng thái khởi đầu:
Bài toán bắt đầu với một bảng 3x3 chứa các số từ 1 đến 8 và một ô trống (0), ví dụ: [[4, 1, 3], [7, 2, 6], [0, 5, 8]]. Đây là trạng thái xuất phát của agent trong quá trình học.
+	Trạng thái đích:
Mục tiêu là đưa lưới về cấu hình chuẩn: [[1, 2, 3], [4, 5, 6], [7, 8, 0]], với ô trống nằm ở góc dưới cùng bên phải.
+	Không gian trạng thái:
Bao gồm tất cả các hoán vị hợp lệ của lưới 3x3, được sinh ra bằng cách di chuyển ô trống để hoán đổi với một ô lân cận. Q-Learning sẽ khám phá dần dần không gian này nhằm học được chính sách hành động tối ưu.
+	Tập hành động:
Tại mỗi trạng thái, agent có thể thực hiện một trong các hành động: lên, xuống, trái, hoặc phải, nếu di chuyển đó hợp lệ (không vượt ra ngoài lưới).
+	Định nghĩa chi phí / phần thưởng:
Trong Q-Learning, khái niệm chi phí được thay thế bằng phần thưởng (reward). Mỗi bước di chuyển được gán một phần thưởng âm nhẹ để khuyến khích tìm đường đi ngắn nhất. Khi agent đạt được trạng thái mục tiêu, nó nhận một phần thưởng dương lớn.
![2 6](https://github.com/user-attachments/assets/1489d316-b176-48ef-9737-a2d46d22b13a)

+	Chiến lược giải:
Q-Learning sử dụng một bảng Q (Q-table) để học giá trị kỳ vọng của mỗi hành động tại mỗi trạng thái, thông qua quá trình thử-sai (exploration) và khai thác (exploitation). Khi đã học xong, agent có thể trích xuất dãy hành động tốt nhất dẫn đến mục tiêu từ bảng Q này.

3. Tác giả
  Dự án được thực hiện bởi:
  Sinh Viên: Trương Tấn Sang - 23110300
  Dự án này là đồ án cá nhân phục vụ việc học tập, đồng thời nhằm mục đích nghiên cứu và ứng dụng các thuật toán tìm kiếm AI vào bài toán 8-Puzzle, với trọng tâm là tối ưu hóa hiệu suất và trải nghiệm người dùng.
4. Tài liệu tham khảo
  +	S. J. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed. Pearson, 2020.
  +	S. J. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 3rd ed., Pearson, 2016.
  +	1 số tool AI như: ChatGPT, Cursor,...

