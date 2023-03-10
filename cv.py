import cv2
import pytesseract

src_img = '/Users/karelomab/Documents/GitHub/sudosolve/sudoku.png'
board_file = "/Users/karelomab/Documents/GitHub/sudosolve/board.txt"
save_images = False

# Load image, grayscale, median blur, sharpen image
img = cv2.imread(src_img)


def proc_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray,50,255,0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours detected:", len(contours))


    block_index = 0

    f = open(board_file, "w+")
    
    for cnt in contours[::-1]:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.1:
                #img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
                #cv2.putText(img, 'S', (x1+40, y1+70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                number_block = img[y:y+h,x:x+w]
                #cv2.imshow("Block {}".format(block_index), number_block)
                #cv2.waitKey(0)

                #extract 3x3 cells from each block
                height, width = number_block.shape[:2]
                cw, ch = width//3, height//3
                margin = 5
                cell_num = 0
                
                
                for i in range(9):
                    buff = []
                    for j in range(9):
                        y = i * ch
                        x = j * cw
                        cell = img[y+margin:y+ch-margin,x+margin:x+cw-margin]

                        try:
                            d = pytesseract.image_to_string(cell, config = '--psm 7 outputbase digits')
                            if not d:
                                if save_images:
                                    cv2.imwrite("cell_{}_empty.png".format(cell_num, cell_num), cell)
                                buff.append('0')    #0 represents empty cell
                            else:
                                if save_images:
                                    cv2.imwrite("cell_{}_{}.png".format(cell_num, d), cell)
                                buff.append(d.strip())
                            print(d)
                        except:
                            pass

                        cell_num += 1
                    #print(buff, " ".join(buff))
                    f.write(" ".join(buff) + "\n")
                    #input()
          
                
                #input()
                f.close()
                return
    
    #cv2.imshow("Board", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

proc_image(img)