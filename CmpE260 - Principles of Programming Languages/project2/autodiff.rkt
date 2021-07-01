; karahan saritas
; 2018400174
; compiling: yes
; complete: yes
#lang racket
(provide (all-defined-out))

;; given
(struct num (value grad)
    #:property prop:custom-write
    (lambda (num port write?)
        (fprintf port (if write? "(num ~s ~s)" "(num ~a ~a)")
            (num-value num) (num-grad num))))


; 3.1) (get-value num-list)          
(define (get-value num-list) 
    (cond ((null? num-list) '())
          ((list? num-list)(cons (car (cdr (car num-list))) (get-value (cdr num-list))))
          (else (num-value num-list))))

; 3.2) (get-grad num-list)
(define (get-grad num-list) 
    (cond ((null? num-list) '())
          ((list? num-list)(cons (car (cdr (cdr (car num-list)))) (get-grad (cdr num-list))))
          (else (num-grad num-list))))

; Difference between get-value and values:
; Given a list of nums, (get-value num-list) doesn't evaluate each num. It considers them as lists, therefore uses car and cdr on them to extract information.
; (values num-list) treats each element of the list as a num. Therefore it applies num-value and num-grad to extract information.

; (values num-list) --> extract the values of nums in a list.
(define (values num-list)
  (cond ((null? num-list) '())
        (else (cons (num-value (car num-list)) (values (cdr num-list))))))
; (grads num-list) --> extract the gradients of nums in a list.
(define (grads num-list)
  (cond ((null? num-list) '())
        (else (cons (num-grad (car num-list)) (grads (cdr num-list))))))

; 4.1) (add num1 num2 ...)
(define (add num1 . others)
  (cond ((null? num1) '())
        ((null? others) (num (num-value num1)(num-grad num1)))
        (else (num (apply + (cons (num-value num1) (values others))) (apply + (cons (num-grad num1)(grads others)))))))

; 4.2) (mul num1 num2 ...)
(define (mul num1 . others)
  (cond ((null? num1) '())
        ((null? others) (num (num-value num1)(num-grad num1)))
        (else (define VAL (cons (num-value num1) (values others))) (define multiplication (apply * VAL))
              (num multiplication (gradient VAL (cons (num-grad num1) (grads others)) 1)))))

; The derivative of mul operator = sum of multiplication of each term's gradient with others' values
(define (gradient values grad soFar)
  (cond ((null? values) 0)
        (else (define sum (* (apply * (cdr values)) soFar)) (+ (* (car grad) sum)  (gradient (cdr values) (cdr grad) (* (car values) soFar))))
        ))

; 4.3) (sub num1 num2 ...)
(define (sub num1 . others)
  (cond ((null? num1) '())
        ((null? others) num1)
        (else (num (apply - (cons (num-value num1) (values others))) (apply - (cons (num-grad num1)(grads others)))))))

; 4.4) relu and mse
(define relu (lambda (x) (if (> (num-value x) 0) x (num 0.0 0.0))))
(define mse (lambda (x y) (mul (sub x y) (sub x y))))

; 5.1) (create-hash names values var)
(define (create-hash names values var)
  (define ht (hash)) 
  (func ht names values var))

; func returns the updated hash-map.
(define (func ht names values var)
  (cond ((null? names) ht)
        (else (func (update-hash ht names values var) (cdr names) (cdr values) var))))

; update-hash updates the hash map.
(define (update-hash ht names values var)
  (cond ((equal? (car names) var) (hash-set ht (car names) (num (car values) 1.0)))
        (else (hash-set ht (car names)(num (car values) 0.0)))))

; 5.2) (parse hash expr)
(define (parse hash expr)
  (cond ((null? expr) expr)
        ((list? expr) (cons (parse hash (car expr)) (parse hash (cdr expr))))
        ((equal? expr '+)  'add)
        ((equal? expr '*) 'mul)
        ((equal? expr '-) 'sub)
        ((equal? expr 'mse) 'mse)
        ((equal? expr 'relu) 'relu)
        ((number? expr) (num expr 0.0))
        (else (hash-ref hash expr))
        ))

; 5.3) (grad names values var expr)
(define (grad names values var expr)
  (cond ((null? expr) expr)
        (else (define hash (create-hash names values var))
        (num-grad (eval(parse hash expr))))))


; 5.4) (partial-grad names values vars expr)
(define (partial-grad names values vars expr) (partial names names values vars expr))

(define (partial names itr values vars expr)
  (cond ((null? itr) itr)
        ((member (car itr) vars) (cons (grad names values (car itr) expr) (partial names (cdr itr) values vars expr)))
        (else (cons 0.0 (partial names (cdr itr) values vars expr)))))

; 5.5) (gradient-descent names values vars lr expr)
(define (gradient-descent names values vars lr expr)
  (define subList (mul-list (partial-grad names values vars expr) lr))
  (map (lambda (num1 num2) (- num1 num2)) values subList))

; multiply each element of a list with x
(define (mul-list lst x)
  (map (lambda (n) (* x n)) lst))

; 5.6) (optimize names values vars lr k expr)
(define (optimize names values vars lr k expr)
  (cond((= k 0) values ) ; no change
       ((= k 1) (gradient-descent names values vars lr expr))
       (else (gradient-descent names (optimize names values vars lr (- k 1) expr) vars lr expr))))
